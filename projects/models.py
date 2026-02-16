from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    total_released = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Branch(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=200)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"
    
    def recalculate_total_spent(self):
        self.total_spent = sum(sb.amount for sb in self.subbranches.all())
        self.save()


class SubBranch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='subbranches')
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.branch.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.branch.recalculate_total_spent()
    
    def delete(self, *args, **kwargs):
        branch = self.branch
        super().delete(*args, **kwargs)
        branch.recalculate_total_spent()


class ReleasedHistory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='released_history')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.project.name} - ₹{self.amount}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update project's total_released
        self.project.total_released = sum(rh.amount for rh in self.project.released_history.all())
        self.project.save()
    
    def delete(self, *args, **kwargs):
        project = self.project
        super().delete(*args, **kwargs)
        # Update project's total_released after deletion
        project.total_released = sum(rh.amount for rh in project.released_history.all())
        project.save()

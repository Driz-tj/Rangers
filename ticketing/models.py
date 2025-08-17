from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files import File


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"


class Match(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('live', 'Live'),
        ('completed', 'Completed'),
    ]
    
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    venue = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.date_time.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['date_time']


class TicketCategory(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Ticket Categories"


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    category = models.ForeignKey(TicketCategory, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(default=timezone.now)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Ticket for {self.match} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.qr_code:
            qr_data = f"Ticket ID: {self.id}, Match: {self.match}, User: {self.user.username}"
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            self.qr_code.save(
                f'ticket_{self.id}_qr.png',
                File(buffer),
                save=False
            )
            super().save(*args, **kwargs)


class News(models.Model):
    CATEGORY_CHOICES = [
        ('match_report', 'Match Report'),
        ('club_news', 'Club News'),
        ('player_news', 'Player News'),
        ('announcement', 'Announcement'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='club_news')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images/', blank=True)
    publish_date = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-publish_date']
        verbose_name_plural = "News"


class Report(models.Model):
    REPORT_TYPES = [
        ('sales', 'Sales Report'),
        ('attendance', 'Attendance Report'),
        ('revenue', 'Revenue Report'),
    ]
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True)
    data = models.JSONField()
    generated_date = models.DateTimeField(default=timezone.now)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.report_type} - {self.generated_date.strftime('%Y-%m-%d')}"

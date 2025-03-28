from fileinput import filename
import os
from django.shortcuts import render,redirect, HttpResponse
from apps.AnnouncementManagement.forms import AnnouncementForm
from .models import Announcement
from django.contrib.auth.decorators import login_required
from .decorators import admin_only
from django.views.decorators.cache import cache_control

# Create your views here.

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url="loginPage")
@admin_only
def announcementPage(request):
    if request.user.is_authenticated:
        return render (request, 'AnnouncementPage/announcement.html')
    else:
        return redirect('loginPage')


@login_required(login_url="loginPage")
@admin_only
def announcement_list(request):
    if request.user.is_authenticated:
        context = {'announcementList': Announcement.objects.all().order_by('-post_date')}
        return render(request, 'AnnouncementPage/announcement_list.html', context)
    else:
        return redirect('loginPage')

@login_required(login_url="loginPage")
@admin_only
def add_announcement(request):
    if request.user.is_authenticated:
        form = AnnouncementForm
        if request.method == 'POST':
            form = AnnouncementForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponse(status=204, headers={'HX-Trigger': 'announcementAdd'})
        return render (request, 'AnnouncementPage/announcement_form.html', {'form': form})
    else:
        return redirect('loginPage')

@login_required(login_url="loginPage")
@admin_only
def edit_announcement(request, id):
    if request.user.is_authenticated:
        edit = Announcement.objects.get(id=id)

        if request.method == "POST":
            # Handle image upload
            if 'image' in request.FILES:
                if edit.image and os.path.exists(edit.image.path):
                    os.remove(edit.image.path)
                edit.image = request.FILES['image']

            # Handle document upload
            if 'document' in request.FILES:
                if edit.document and os.path.exists(edit.document.path):
                    os.remove(edit.document.path)
                edit.document = request.FILES['document']

            # Handle document removal
            if 'document_removed' in request.POST and edit.document:
                if os.path.exists(edit.document.path):
                    os.remove(edit.document.path)
                edit.document = None

            # Update text fields
            edit.title = request.POST.get('title')
            edit.body = request.POST.get('body')
            edit.save()
            return redirect('announcementPage')

        context = {'edit': edit}
        return render(request, 'AnnouncementPage/edit_announcement.html',context)
    else:
        return redirect('loginPage')

@login_required(login_url="loginPage")
@admin_only
def delete_announcement(request, id):
    if request.user.is_authenticated:
        ann = Announcement.objects.get(id=id)

        context = {'ann': ann}
        if request.method == 'POST':
            # Check if announcement has an image and if the file exists
            if ann.image and ann.image.name and os.path.exists(ann.image.path):
                os.remove(ann.image.path)

            # Check if announcement has a document and if the file exists
            if ann.document and ann.document.name and os.path.exists(ann.document.path):
                os.remove(ann.document.path)

            # Delete the announcement object
            ann.delete()
            return redirect('announcementPage')

        return render(request, 'AnnouncementPage/delete_announcement.html', context)
    else:
        return redirect('loginPage')

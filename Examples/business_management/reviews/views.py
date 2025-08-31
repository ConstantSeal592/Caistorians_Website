from django.shortcuts import render

def review_list(request, salon_id):
    return render(request, 'reviews/review_list.html')

def review_form(request, salon_id):
    return render(request, 'reviews/review_form.html')

def review_moderation(request):
    return render(request, 'reviews/review_moderation.html')

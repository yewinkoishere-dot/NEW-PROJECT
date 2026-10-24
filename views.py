from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Exam, Submission, Choice


@login_required
def submit(request, course_id):
    if request.method == "POST":
        exam = get_object_or_404(Exam, course_id=course_id)
        submission = Submission.objects.create(
            exam=exam,
            student=request.user,
        )

        score = 0
        for choice_id in request.POST.getlist("choices"):
            choice = get_object_or_404(Choice, id=choice_id)
            submission.choices.add(choice)
            if choice.is_correct:
                score += choice.question.grade

        submission.total_score = score
        submission.save()
        return redirect("show_exam_result", course_id=course_id)

    return redirect("course_details", course_id=course_id)


@login_required
def show_exam_result(request, course_id):
    exam = get_object_or_404(Exam, course_id=course_id)
    submission = Submission.objects.filter(
        exam=exam, student=request.user
    ).order_by("-id").first()

    if submission is None:
        return redirect("course_details", course_id=course_id)

    return render(
        request,
        "onlinecourse/exam_result_bootstrap.html",
        {"submission": submission, "exam": exam},
    )

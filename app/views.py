from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from appointment_search.models import AppointmentSchedule


class RemoveAppointmentsView(TemplateView):
    template_name = 'admin/remove_appointments.html'


@staff_member_required
def delete_appointments(request):
    if request.method == 'POST' and request.body:
        from_date = request.POST['from-date']
        to_date = request.POST['to-date']
        result = AppointmentSchedule.objects.filter(date__date__gte=from_date, date__date__lte=to_date)
        result_message = "Deleted {} Appointments.".format(result.count())
        result.delete()
        messages.add_message(request, messages.INFO, result_message)
        return HttpResponseRedirect(reverse('admin:index'))
    raise Http404


@staff_member_required
def confirm_delete(request):
    if request.method == 'POST' and request.body:
        from_date = request.POST['from-date']
        to_date = request.POST['to-date']
        result = AppointmentSchedule.objects.filter(date__date__gte=from_date, date__date__lte=to_date).values('registration_number', 'date')
        context = {'appointments': list(result), 'from_date': from_date, 'to_date': to_date}
        return render(request, 'admin/confirm_delete.html', context)
    raise Http404

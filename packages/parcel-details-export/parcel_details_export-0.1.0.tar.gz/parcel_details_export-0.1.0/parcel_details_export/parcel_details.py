from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from django.shortcuts import get_object_or_404

def export_parcel_pdf(model, parcel_id, payment_attr="payment"):
    parcel = get_object_or_404(model, pk=parcel_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="parcel_{parcel.tracking_number}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title = f"Parcel Report - {parcel.tracking_number}"
    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))

    details = f"""
        <b>Status:</b> {parcel.get_status_display()}<br/>
        <b>Sender:</b> {parcel.sender}<br/>
        <b>Receiver:</b> {parcel.receiver_name}<br/>
        <b>Phone:</b> {parcel.receiver_phone}<br/>
        <b>Address:</b> {parcel.receiver_address}<br/>
        <b>Weight:</b> {parcel.weight} kg<br/>
        <b>Type:</b> {parcel.get_parcel_type_display()}<br/>
        <b>Dimensions:</b> {parcel.dimensions}<br/>
        <b>Description:</b> {parcel.description}<br/>
        <b>Created At:</b> {parcel.created_at}<br/>
    """
    story.append(Paragraph(details, styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    if hasattr(parcel, payment_attr):
        pay = getattr(parcel, payment_attr)
        payment_details = f"""
            <b>Amount:</b> {pay.amount}<br/>
            <b>Status:</b> {pay.get_payment_status_display()}<br/>
            <b>method:</b> {pay.get_payment_method_display()}<br/>
            <b>Transaction ID:</b> {pay.transaction_id or 'N/A'}<br/>
        """
        story.append(Paragraph("<b>Payment Details</b>", styles["Heading3"]))
        story.append(Paragraph(payment_details, styles["Normal"]))

    doc.build(story)
    return response

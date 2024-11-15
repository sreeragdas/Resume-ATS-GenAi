from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai
import fitz #PyMuPDF
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to images using PyMuPDF
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = pdf_document.load_page(0)

        pix = first_page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr.getvalue()).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")





submit3 = st.button("Percentage match")


input_prompt3 = """
You are an advanced ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate a candidate's resume against the provided job description by calculating a match percentage based on how 
closely the resume aligns with the job description, and providing an overall match score. Identify any critical keywords or skills 
mentioned in the job description that are missing from the resume, and then analyze the resume’s content to infer the type of job 
profile that best suits the candidate’s skills, experience, and qualifications, recommending a suitable job profile or role based 
on this analysis. Conclude with a brief summary evaluating the candidate's strengths and areas for improvement in relation to the 
job requirements, highlighting how well the resume meets the needs of the position, any notable gaps, and suggested areas for growth. 
This evaluation should include a match score, a summary of missing keywords or skills, a recommendation for the most suitable job 
profile, and constructive feedback on the candidate’s strengths and improvement areas.

"""



if submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
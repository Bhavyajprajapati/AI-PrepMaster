import tempfile
import streamlit as st
import cv2
import numpy as np
import io
from fpdf import FPDF
import fitz  # PyMuPDF
from PIL import Image
# Function to reorder points for perspective transformation
def reorder(myPoints):
    if myPoints.shape[0] != 4:
        return None
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew

# Function to find rectangle contours
def rectContour(contours):
    rectCon = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if len(approx) == 4:
                rectCon.append(i)
    return sorted(rectCon, key=cv2.contourArea, reverse=True)

# Function to get corner points
def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True)
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True)
    return approx if len(approx) == 4 else None

# Function to split the image into boxes
def splitBoxes(img, questions, choices):
    rows = np.vsplit(img, questions)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, choices)
        boxes.extend(cols)
    return boxes

# Function to draw grid on the image
def drawGrid(img, questions, choices):
    secW = int(img.shape[1] / choices)
    secH = int(img.shape[0] / questions)
    for i in range(questions + 1):
        cv2.line(img, (0, secH * i), (img.shape[1], secH * i), (255, 255, 0), 2)
    for i in range(choices + 1):
        cv2.line(img, (secW * i, 0), (secW * i, img.shape[0]), (255, 255, 0), 2)
    # st.image(img)
    return img

# Function to show answers on the image
def showAnswers(img, myIndex, grading, ans, questions, choices):
    secW = img.shape[1] // choices
    secH = img.shape[0] // questions
    for x in range(questions):
        if myIndex[x] == -1:
            # No answer marked
            correctX, correctY = (ans[x] * secW) + secW // 2, (x * secH) + secH // 2
            cv2.putText(img, "X", (correctX, correctY), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            # cv2.putText(img, "X", (secW * 2, (x * secH) + secH // 2), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            continue
        cX, cY = (myIndex[x] * secW) + secW // 2, (x * secH) + secH // 2
        # cv2.circle(img, (cX, cY), 20, (0, 255, 0) if grading[x] else (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (cX, cY), 30, (0, 255, 0) if grading[x] else (0, 0, 255), cv2.FILLED)

        correctX, correctY = (ans[x] * secW) + secW // 2, (x * secH) + secH // 2
        cv2.circle(img, (correctX, correctY), 20, (0, 255, 0), cv2.FILLED)

# Function to calculate the score with negative marking
def calculate_score(grading, negative_count, negative_marking, questions):
    correct_answers_count = sum(grading)
    score = correct_answers_count - (negative_count * negative_marking)
    return max(0, score)  # Ensure the score is not negative

def pdf_to_images(pdf_file):
    images = []
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(np.array(img))
    return images

def omr_checking_interface():
    st.subheader("OMR Sheet Checking")
    
    uploaded_files = st.file_uploader("Upload OMR sheet images",help="Multiple images are also allowed", type=["jpg", "png", "jpeg" ,"pdf"], accept_multiple_files=True)
    questions = st.selectbox("Number of Questions", options=[10, 15, 20, 25,30])
    negative_marking = st.number_input("Negative Marking Value", min_value=0.0, value=0.0)
    choices = st.number_input("Number of Choices", min_value=4,max_value=5)

    # User input for correct answers
    correct_answers_input = st.text_input(
        "Enter Correct Answers",
        help="Comma-separated values (e.g., A,B,C,...)",
        # value="A,B,C,D,A,A,C,A,D,A"
    )

    
    if correct_answers_input:
        # Mapping letters to numbers
        choices_map = {chr(65 + i): i for i in range(choices)}  # {'A': 0, 'B': 1, ..., 'F': 5 (if choices=6)}

        # Validate and convert input
        try:
            correct_answers_list = correct_answers_input.split(',')
            
            # Check if all letters exist in choices_map
            if not all(letter in choices_map for letter in correct_answers_list):
                st.error(f"Invalid answer(s). Please use letters between A and {chr(64 + choices)}.")
            else:
                ans = [choices_map[letter] for letter in correct_answers_list]

                # Check if number of answers matches the number of questions
                if len(ans) != questions:
                    st.error(f"The number of answers provided doesn't match the number of questions ({questions}).")
        except Exception as e:
            st.error(f"Error processing input: {e}")
        

    if questions == 15:
        heightImg = 1500
        widthImg = 900
        if choices == 4:
            widthImg = 900

    elif questions == 20:
        heightImg = 1800
        widthImg = 1000
        if choices == 4:
            heightImg = 1000
            widthImg = 900
    elif questions == 30:
        heightImg = 3000
        widthImg = 1400
        if choices == 5:   
            heightImg = 3000 
            widthImg = 1400
    elif questions == 10 and choices == 4:
        heightImg = 1400
        widthImg = 1200
    elif questions == 25:
        if choices == 5:
            heightImg = 1400
            widthImg = 1200
        else:
            heightImg = 1400
            widthImg = 1200
    else:
        heightImg = 1400
        widthImg = 1400
    

    
    
        
    if uploaded_files and st.button("Check OMR Sheet"):
        processed_images = []
        
        images = []
        with st.status("Processing images...",expanded=True) as status:
            for uploaded_file in uploaded_files:
                if uploaded_file.type == "application/pdf":
                    # Convert PDF to images
                    images_t = pdf_to_images(uploaded_file)
                    for img in images_t:
                        # img = cv2.resize(img, (widthImg, heightImg))
                        images.append(img)
                else:
                    # Process image files
                    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                    img = cv2.imdecode(file_bytes, 1)
                    images.append(img)
        
            
            
            for uploaded_file in images:
                # file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                # img = cv2.imdecode(file_bytes, 1)
                
                        
                

                img = cv2.resize(uploaded_file, (widthImg, heightImg))
                imgFinal = img.copy()
                imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # st.image(imgGray)
                imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
                imgCanny = cv2.Canny(imgBlur, 10, 70)
                # st.image(imgCanny)

                try:
                    contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                    rectCon = rectContour(contours)

                    if len(rectCon) < 2:
                        st.error("Not enough rectangles found")
                    else:
                        biggestPoints, gradePoints = getCornerPoints(rectCon[0]), getCornerPoints(rectCon[1])
                        if biggestPoints is None or gradePoints is None:
                            st.error("Could not get corner points")
                        else:
                            biggestPoints = reorder(biggestPoints)
                            pts1 = np.float32(biggestPoints)
                            pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
                            matrix = cv2.getPerspectiveTransform(pts1, pts2)
                            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

                            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
                            imgThresh = cv2.threshold(imgWarpGray, 170, 255, cv2.THRESH_BINARY_INV)[1]

                            boxes = splitBoxes(imgThresh, questions, choices)
                            myPixelVal = np.array([cv2.countNonZero(box) for box in boxes]).reshape(questions, choices)
                            negative_count = 0
                            wrong_count = 0
                            not_attended = 0
                            myIndex = []
                            comp = 2500
                            # 2500 is working good for 25 question
                            if questions == 15:
                                comp = 3000
                            if questions == 20 and choices == 4:
                                comp = 2000
                            if questions == 30:
                                comp = 5300
                                if choices == 5:
                                    comp = 5300 #values are coming near to 5300 for both marked and unmarked 
                            if questions == 10:
                                comp = 7000
                            for i, row in enumerate(myPixelVal):
                                # print(i)
                                # print(row)
                                max_val = np.max(row)
                                # marked_indices = np.where(row >= max_val - 500)[0]  # Allow small variations due to noise
                                if questions == 15:
                                    # marked_indices = np.where(row >= max_val - 800)[0]  # Allow small variations due to noise
                                    # marked_indices = np.where(row >= max_val - 1000)[0]  # Allow small variations due to noise
                                    marked_indices = np.where(row >= max_val - 1500)[0]  # Allow small variations due to noise
                                elif questions == 10:
                                    if choices == 5:
                                        marked_indices = np.where(row >= max_val - 1500)[0]  # Allow small variations due to noise
                                    else:
                                        marked_indices = np.where(row >= max_val - 800)[0]  # Allow small variations due to noise
                                else:
                                    marked_indices = np.where(row >= max_val - 700)[0]  # Allow small variations due to noise
                                # print(max_val)
                                # print(row)
                                
                                # because if no one is marked then all are nearer to each other and so i recieve
                                # it as all marked if i not add < 2000 condition
                                if max_val < comp or len(marked_indices)==0:
                                    myIndex.append(-1)  # No answer marked
                                    not_attended+=1
                                    wrong_count += 1
                                elif len(marked_indices) > 1:
                                    myIndex.append(-1)  # Multiple answers marked
                                    negative_count += 1
                                    wrong_count += 1
                                    # print("\n")
                                    # print(f"row is {i}")
                                    # print(row)
                                    # print(marked_indices)
                                    # print("\n")
                                else:
                                    myIndex.append(marked_indices[0])
                                    if marked_indices[0] != ans[i]:
                                        negative_count += 1
                                        wrong_count += 1
                                        # print("\n")
                                        # print(f"row is {i}")
                                        # print(marked_indices)
                                        # print("\n")

                            # Grading with Negative Marking
                            grading = [1 if myIndex[i] == ans[i] else 0 for i in range(questions)]

                            score = calculate_score(grading, negative_count, negative_marking, questions)
                            showAnswers(imgWarpColored, myIndex, grading, ans, questions, choices)
                            drawGrid(imgWarpColored, questions, choices)

                            # Display score and correct answers count in the app
                            st.write(f"**Score:** {score}")
                            # below is just writing out of not dividing..
                            st.write(f"**Correct Answers:** {sum(grading)}/{questions}")
                            # st.write(f"**wrong Answers:** {wrong_count}/{questions}")
                            st.write(f"**Negative Counts:** {negative_count}/{questions}")
                            st.write(f"**Not attempted:** {not_attended}/{questions}")

                            # Add score and correct answers to the image
                            cv2.putText(imgWarpColored, f"Score: {(score)}%", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                            cv2.putText(imgWarpColored, f"Correct: {sum(grading)}/{questions}", (50, 100),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                            
                        

                            st.image(imgWarpColored, caption='Processed OMR Sheet', use_column_width=True)
                            
                            # code to transfer colors to main image
                            imgRawDrawing = np.zeros_like(imgWarpColored)
                            showAnswers(imgRawDrawing, myIndex, grading, ans, questions, choices)
                            drawGrid(imgRawDrawing, questions, choices)
                            invMatrix = cv2.getPerspectiveTransform(pts2, pts1)
                            imgInvWarp = cv2.warpPerspective(imgRawDrawing, invMatrix, (widthImg, heightImg))
                            
                            #now just combine imgInvWrap with main img
                            
                            # imgFinal = cv2.addWeighted(imgFinal, 0.7, imgInvWarp, 1.3, 0)
                            imgFinal = cv2.addWeighted(imgFinal, 0.6, imgInvWarp, 8.9, 0)
                            # Add score and correct answers to the image
                            
                            if questions == 30:
                                if choices == 4:
                                    cv2.putText(imgFinal, f"Score: {(score)}%", (880, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Correct: {sum(grading)}/{questions}", (880, 480),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    # cv2.putText(imgFinal, f"wrong: {wrong_count}/{questions}", (550, 310),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Negative Counts: {negative_count}/{questions}", (880, 510),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Not attempted: {not_attended}/{questions}", (880, 540),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                else:
                                    cv2.putText(imgFinal, f"Score: {(score)}%", (850, 430), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Correct: {sum(grading)}/{questions}", (850, 460),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    # cv2.putText(imgFinal, f"wrong: {wrong_count}/{questions}", (550, 310),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Negative Counts: {negative_count}/{questions}", (850, 490),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Not attempted: {not_attended}/{questions}", (850, 520),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

                            elif questions == 25:
                                if choices == 5:
                                    cv2.putText(imgFinal, f"Score: {(score)}%", (670, 160), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Correct: {sum(grading)}/{questions}", (670, 190),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    # cv2.putText(imgFinal, f"wrong: {wrong_count}/{questions}", (850, 310),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Negative Counts: {negative_count}/{questions}", (670, 220),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Not attempted: {not_attended}/{questions}", (670, 250),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

                                else:
                                    cv2.putText(imgFinal, f"Score: {(score)}%", (670, 160), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Correct: {sum(grading)}/{questions}", (670, 190),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    # cv2.putText(imgFinal, f"wrong: {wrong_count}/{questions}", (850, 310),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Negative Counts: {negative_count}/{questions}", (670, 220),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Not attempted: {not_attended}/{questions}", (670, 250),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                
                            elif questions == 15:
                                if choices == 5:
                                    cv2.putText(imgFinal, f"Score: {(score)}%", (510, 160), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Correct: {sum(grading)}/{questions}", (510, 190),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    # cv2.putText(imgFinal, f"wrong: {wrong_count}/{questions}", (850, 310),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Negative Counts: {negative_count}/{questions}", (510, 220),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Not attempted: {not_attended}/{questions}", (510, 250),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                else:
                                    cv2.putText(imgFinal, f"Score: {(score)}%", (510, 160), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Correct: {sum(grading)}/{questions}", (510, 190),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    # cv2.putText(imgFinal, f"wrong: {wrong_count}/{questions}", (850, 310),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Negative Counts: {negative_count}/{questions}", (510, 220),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Not attempted: {not_attended}/{questions}", (510, 250),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

                            elif questions == 10:
                                if choices == 5:
                                    cv2.putText(imgFinal, f"Score: {(score)}%", (770, 160), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Correct: {sum(grading)}/{questions}", (770, 190),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    # cv2.putText(imgFinal, f"wrong: {wrong_count}/{questions}", (850, 310),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Negative Counts: {negative_count}/{questions}", (770, 220),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Not attempted: {not_attended}/{questions}", (770, 250),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                else:
                                    cv2.putText(imgFinal, f"Score: {(score)}%", (700, 160), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Correct: {sum(grading)}/{questions}", (700, 190),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    # cv2.putText(imgFinal, f"wrong: {wrong_count}/{questions}", (850, 310),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Negative Counts: {negative_count}/{questions}", (700, 220),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Not attempted: {not_attended}/{questions}", (700, 250),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                
                            elif questions == 20:
                                if choices == 4:
                                    cv2.putText(imgFinal, f"Score: {(score)}%", (510, 110), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Correct: {sum(grading)}/{questions}", (510, 140),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    # cv2.putText(imgFinal, f"wrong: {wrong_count}/{questions}", (850, 310),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Negative Counts: {negative_count}/{questions}", (510, 170),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Not attempted: {not_attended}/{questions}", (510, 200),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                else:
                                    cv2.putText(imgFinal, f"Score: {(score)}%", (580, 190), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Correct: {sum(grading)}/{questions}", (580, 220),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    # cv2.putText(imgFinal, f"wrong: {wrong_count}/{questions}", (850, 310),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Negative Counts: {negative_count}/{questions}", (580, 250),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    cv2.putText(imgFinal, f"Not attempted: {not_attended}/{questions}", (580, 280),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                
                            else:
                                cv2.putText(imgFinal, f"Score: {(score)}%", (850, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                cv2.putText(imgFinal, f"Correct: {sum(grading)}/{questions}", (850, 150),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                        
                            # st.image(img)
                            # st.image(imgInvWarp)
                            # st.image(imgFinal)
                except Exception as e:
                    st.error(f"Error: {e}")    

                
                
                
                
                
                
                
                
                
                
                
                # processed_image = imgFinal
                # img = cv2.resize(img, (widthImg, heightImg))
                if questions == 30:
                    processed_image = cv2.resize(imgFinal,(1000,1400))
                else:
                    processed_image = imgFinal
                # processed_images.append((uploaded_file.name, processed_image))
                processed_images.append(processed_image)
                st.image(processed_image, caption=f"Processed: image", use_column_width=True, channels="GRAY")
                # st.image(processed_image, caption=f"Processed: {uploaded_file.name}", use_column_width=True, channels="GRAY")
            status.update(label="Processing complete!", state="complete", expanded=False)  # Finish status


        
        
        if processed_images:
            pdf = FPDF()
            with st.status("Generating pdf...",expanded=True)as status:
                # for image_name, image in processed_images:
                for image in processed_images:
                    # Save the image to a temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                        cv2.imwrite(tmpfile.name, image)
                        # Add a page to the PDF
                        pdf.add_page()
                        # Add the image to the PDF
                        pdf.image(tmpfile.name, x=10, y=10, w=190)  # Adjust dimensions as needed
                        # Optionally, add the image name as a caption
                        # pdf.set_font("Arial", size=12)
                        # pdf.cell(200, 10, txt=image_name, ln=True, align="C")
            status.update(label="Pdf generated!", state="complete", expanded=False)  # Finish status

        # Save the PDF to a BytesIO object
        pdf_bytes = io.BytesIO()
        pdf.output(pdf_bytes)
        pdf_bytes.seek(0)

        # Provide a download button for the PDF
        st.download_button(
            label="Download All Processed Images as PDF",
            data=pdf_bytes,
            file_name="processed_omr_sheets.pdf",
            mime="application/pdf"
        )
        
        
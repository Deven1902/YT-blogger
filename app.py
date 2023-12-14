import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import spacy 

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        return f"Error: {e}"

# def generate_blog_outline(transcript):
#     # Combine the transcript into a single passage
#     full_transcript = " ".join([entry['text'] for entry in transcript])

#     # Load the SpaCy English model
#     nlp = spacy.load("en_core_web_sm")

#     # Process the transcript using SpaCy
#     doc = nlp(full_transcript)

#     # Generate a basic blog outline
#     outline = {"Introduction": [], "Body": [], "Conclusion": []}

#     for sentence in doc.sents:
#         # Analyze sentence sentiment
#         sentiment = "Positive" if sentence.sentiment > 0 else "Negative" if sentence.sentiment < 0 else "Neutral"

#         # Categorize sentences into introduction, body, or conclusion based on position
#         if sentence.start < len(doc) * 0.2:
#             outline["Introduction"].append({"text": sentence.text, "sentiment": sentiment})
#         elif sentence.start > len(doc) * 0.8:
#             outline["Conclusion"].append({"text": sentence.text, "sentiment": sentiment})
#         else:
#             outline["Body"].append({"text": sentence.text, "sentiment": sentiment})

#     return outline 
    
# Inside the generate_blog_outline function
def generate_blog_outline(transcript):
    # Combine the transcript into a single passage
    full_transcript = " ".join([entry['text'] for entry in transcript])

    # Load the SpaCy English model
    nlp = spacy.load("en_core_web_sm")

    # Process the transcript using SpaCy
    doc = nlp(full_transcript)

    # Generate a basic blog outline
    outline = {"Introduction": [], 
                "Body": [], 
                "Conclusion": [], 
                # "Topics": [], 
                # "Keywords": []
                }

    # # Extract topics using SpaCy
    # for entity in doc.ents:
    #     if entity.label_ == "ORG" or entity.label_ == "PERSON":
    #         outline["Topics"].append({"text": entity.text, "label": entity.label_})

    # # Extract keywords using SpaCy
    # for token in doc:
    #     if token.is_alpha and token.is_stop is False:
    #         outline["Keywords"].append({"text": token.text, "pos": token.pos_})

    for sentence in doc.sents:
        # Analyze sentence sentiment
        sentiment = "Positive" if sentence.sentiment > 0 else "Negative" if sentence.sentiment < 0 else "Neutral"

        # Categorize sentences into introduction, body, or conclusion based on position
        if sentence.start < len(doc) * 0.2:
            outline["Introduction"].append({"text": sentence.text, "sentiment": sentiment})
        elif sentence.start > len(doc) * 0.8:
            outline["Conclusion"].append({"text": sentence.text, "sentiment": sentiment})
        else:
            outline["Body"].append({"text": sentence.text, "sentiment": sentiment})

    return outline

def main():
    st.title("YouTube Transcript Blog Outline Generator")

    # Get YouTube video URL from the user
    video_url = st.text_input("Enter YouTube Video URL:")

    if st.button("Generate Blog Outline"):
        # Extract video ID from the URL
        video_id = video_url.split("v=")[1] if "v=" in video_url else None

        if video_id:
            # Fetch the transcript
            transcript = fetch_transcript(video_id)
            st.write("Transcript:")

            # Display the consolidated transcript
            full_transcript = " ".join([entry['text'] for entry in transcript])
            st.write(full_transcript)

            # Generate and display the blog outline
            st.write("\nGenerated Blog Outline:")
            blog_outline = generate_blog_outline(transcript)
            st.write(blog_outline)

        else:
            st.warning("Invalid YouTube URL. Please provide a valid URL.")

if __name__ == "__main__":
    main()

from flask import Flask,render_template,request

from transformers import PegasusForConditionalGeneration,PegasusTokenizer


app=Flask(__name__)

model=PegasusForConditionalGeneration.from_pretrained("C:/Users/91967/OneDrive/Desktop/Nlp project/model")
tokenizer=PegasusTokenizer.from_pretrained("C:/Users/91967/OneDrive/Desktop/Nlp project/tokenizer")

def get_response(input_text, num_return_sequences=5, num_beams=12):
    num_return_sequences = int(num_return_sequences)  # Convert to integer
    batch = tokenizer([input_text], truncation=True, padding='longest', max_length=60, return_tensors="pt")
    translated = model.generate(**batch, max_length=60, num_beams=num_beams, num_return_sequences=num_return_sequences, temperature=1.5)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
    return tgt_text



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/paraphrase', methods=['POST'])
def generate():
    if request.method == 'POST':
        input_text = request.form.get('text')
        num_paraphrases = request.form.get('num_paraphrases')

        paraphrases = get_response(input_text,num_return_sequences=num_paraphrases,num_beams=12)
        print(paraphrases)

        return render_template('index.html', input_text=input_text, paraphrases=paraphrases)
    return render_template('index.html')



if __name__== '__main__':
    app.run(debug=True)
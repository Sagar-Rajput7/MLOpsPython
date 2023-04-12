import torch
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request, send_from_directory

model = torch.hub.load('pytorch/vision:v0.9.0',
                       'squeezenet1_1', pretrained=True)
model.eval()

with open('synset.txt', 'r') as f:
    labels = [l.rstrip() for l in f]

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

app = Flask(__name__)

with app.app_context():

    @app.route('/')
    def index():
        return send_from_directory('static','index.html')
    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)
    @app.route('/predict', methods=['POST'])
    def predict():        	
        print(request.files)
        if 'image' not in request.files:
            # send error response if no input file attached
            return jsonify({'error': 'No file uploaded'}), 400 
        file = request.files['image']
        image = Image.open(file.stream)
        img_tensor = transform(image).unsqueeze(0)
        with torch.no_grad():
            outputs = model(img_tensor)
        scores = torch.nn.functional.softmax(outputs[0], dim=0).numpy()
        sorted_scores = sorted(
            enumerate(scores), key=lambda x: x[1], reverse=True)[:5]
        results = []
        for idx, score in sorted_scores:
            result = {'class': labels[idx], 'probability': str(score)}
            results.append(result)
            print('class=%s ; probability=%f' % (labels[idx], score))

        return jsonify({'results': results})


    # # Enter path to the inference image below
    # img_path1 = 'test.png'
    # predict(img_path1)

    # img_path2 = 'kitten.jpg'
    # predict(img_path2)

    if __name__ == '__main__':
        app.run(debug=True)

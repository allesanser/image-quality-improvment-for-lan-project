import os.path
import os
from flask import Flask, \
    render_template, \
    redirect, \
    request, \
    send_from_directory
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = f'{os.path.join(os.path.dirname(__file__))}uploads/video/'
MEDIA_FOLDER = f'{os.path.join(os.path.dirname(__file__))}' \
               f'static/media/'

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    if request.method == 'GET':
        return render_template('main.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']

        filename = secure_filename(file.filename)
        # print('//////////////////////////////////////////////////////')
        # print(os.path.join(UPLOAD_FOLDER, filename))
        # print('//////////////////////////////////////////////////////')
        file.save(os.path.join(UPLOAD_FOLDER, filename))


        os.system(f'ffmpeg -i {UPLOAD_FOLDER}{filename} -qscale:v 1 -qmin 1 -qmax 1 -vsync 0  {UPLOAD_FOLDER}/frame%08d.png')
        os.remove(f'{UPLOAD_FOLDER}{filename}')
        

        # track.py
        

        file_list = os.listdir('uploads/video/')
        last = file_list[-1]
        # print('//////////////////////////////////////////////////////')
        # print(*file_list)

        # print('//////////////////////////////////////////////////////')
        my_file = open("uploads/spis.txt", "w+")
        for line in sorted(file_list):
                my_file.write(line)
                if line != last:
                        my_file.write('\n')
        # до этого момента все работает

        # os.system(f'python3 iSeeBetterTest.py --data_dir {UPLOAD_FOLDER} --file_list uploads/spis.txt -c --testBatchSize 1')
        # раскоментировать, чтобы начать улучшать качество, а верхнюю закоментить
        os.system(f'python3 iSeeBetterTest.py --data_dir {UPLOAD_FOLDER} --file_list spis.txt -c --testBatchSize 1 --upscale_only ')

        
        
        os.system("ffmpeg -r 30 -pattern_type glob -i 'Results/*_RBPNF7.png' -c:v libx264 -vf fps=30 -pix_fmt yuv420p uploads/out.mp4")
        os.system('rm uploads/video/*')

        return send_from_directory('uploads/', 'out.mp4', as_attachment=True)

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
import requests


def add_movie(server_url, video_path):
    data = {'video_path': video_path}
    response = requests.post(f'{server_url}/add_movie/', json=data)

    if response.status_code == 200:
        print(f'Successfully added movie: {video_path}')
    else:
        print(f'Error adding movie: {video_path}')
        print(response.json())


if __name__ == '__main__':
    server_urls = 'http://127.0.0.1:5001', 'http://127.0.0.1:5002'

    # Add video.mp4
    video_path_1 = 'hls-server/media/video.mp4'
    add_movie(server_urls[0], video_path_1)

    # Add video1.mp4
    video_path_2 = 'hls-server/media/video2.mp4'
    add_movie(server_urls[1], video_path_2)

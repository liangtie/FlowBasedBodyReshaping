import json
import requests

def test_body_shaping_api(file_path, degree, roi):
    url = 'http://127.0.0.1:7565/body_shaping'
    
    # Prepare the files and data
    files = {'file': open(file_path, 'rb')}
    json_data = {'degree': degree, 'roi': roi}

    data = {'json': json.dumps(json_data)}

    # Send the POST request
    response = requests.post(url, files=files, data=data)
    
    # Handle the response
    if response.status_code == 200:
        # Save the reshaped image
        with open('reshaped_image.jpg', 'wb') as f:
            f.write(response.content)
        print("Reshaped image saved as 'reshaped_image.jpg'")
    else:
        # Print the error message
        print(f"Error: {response.status_code} - {response.json()['error']}")

if __name__ == '__main__':
    # Path to the image file you want to test with
    file_path = 'test.jpg'

    degree = 1.0  # 美型程度0.1 ~ 1.0
    roi = 2 # 0: 胳膊 ; 1 :腿 ; 2 : 全身

    # Test the API
    test_body_shaping_api(file_path, degree, roi)

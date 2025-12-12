import os

image_name_dict = {
    'aircraft'        : 'aircraft.jpg',
    'aircraft_mask'   : 'aircraft_mask.png',
    'shapes'          : 'shapes.png',
    'woman'           : 'woman.png',
    'lambo'           : 'lambo.png',
    'lena'            : 'lena.png',
    'bird'            : 'bird.jpg',
    'brick'           : 'brick.png',
    'cat'             : 'cat.png',
    'coffee'          : 'coffee.png',
    'dog'             : 'dog.png',
    'horse'           : 'horse.jpg',
    'page'            : 'page.png',
}

def pyzjr_datas(image_name=None):
    script_path = os.path.dirname(os.path.abspath(__file__))
    if image_name:
        image_name = image_name_dict[image_name]
        image_path = os.path.join(script_path, f'images/{image_name}')
    else:
        image_path = []
        all_image_paths = [image_name_dict[key] for key in image_name_dict]
        for img_name in all_image_paths:
            im_path = os.path.join(script_path, f'images/{img_name}')
            image_path.append(im_path)
    return image_path


if __name__=="__main__":
    from pyzjr.visualize import read_bgr, display
    print(pyzjr_datas())
    img = read_bgr(pyzjr_datas()[5])
    display(img)

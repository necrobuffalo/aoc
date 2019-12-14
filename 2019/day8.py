LAYER_WIDTH = 25
LAYER_HEIGHT = 6
LAYER_SIZE = LAYER_WIDTH * LAYER_HEIGHT

def render(image: str, width=LAYER_WIDTH, height=LAYER_HEIGHT) -> None:
    for i in range(0, len(image), LAYER_WIDTH):
        print(image[i:i+LAYER_WIDTH].replace("0", " ").replace("1", "#"))

raw_image = input().strip()
layers = [raw_image[i:i+LAYER_SIZE] for i in range(0,len(raw_image),LAYER_SIZE)]

least_zeroes = min(layers, key=lambda l: l.count('0'))
print("1s multiplied by 2s: {}".format(least_zeroes.count('1') * least_zeroes.count('2')))

print("Parsing image")
parsed_image_list = ['2' for i in range(LAYER_SIZE)]
for l in layers:
    for i in range(LAYER_SIZE):
        if parsed_image_list[i] == '2':
            parsed_image_list[i] = l[i]
    if parsed_image_list.count('2') == 0:
        # Stop if we have no more transparent pixels
        break

render(''.join(parsed_image_list))

import sys
import mosaic
# Set some globals
RANGE_OF_COLOURS = 3
NUMBER_OF_ARGUMENTS = 5

# Calculate the distance between two pixels
def compare_pixel(pixel1, pixel2):
    distance = 0
    for colour in range(RANGE_OF_COLOURS):
        distance += abs(pixel1[colour]-pixel2[colour])
    return distance

# Calculate the total distance between two photos
def compare(image1, image2):
    # Set the working parameters for length and width
    height1 = len(image1)
    height2 = len(image2)
    width1 = len(image1[0])
    width2 = len(image2[0])
    height = min(height1, height2)
    width = min(width1, width2)

    # Compare all the pixels one by one
    distance = 0
    for row in range(height):
        for column in range(width):
            distance += compare_pixel(image1[row][column],image2[row][column])

    return distance

# A function that get a piece of an image
def get_piece(image, upper_left, size):
    # working parameters which takes into account the image bounds
    image_height = len(image)
    image_width = len(image[0])
    if upper_left[0] + size[0] <= image_height:
        working_width = size[0]
    else:
        working_width = image_height - upper_left[0]
    if upper_left[1] + size[1] <= image_width:
        working_height = size[1]
    else:
        working_height = image_width - upper_left[1]

    # Set an empty result image to write on
    result = [[0 for i in range(working_width)] for j in range(working_height)]

    # Write on one cell at a time
    for row in range(working_height):
        for column in range(working_width):
            result[row][column] = image[(size[0]+row)][(size[1]+column)]

    return result
#TODO: test this function

def set_piece(image, upper_left, piece):
    # Set working parameters
    image_height = len(image)
    image_width = len(image[0])
    crop_height = len(piece)
    crop_width = len(piece[0])

    if upper_left[0] + crop_height <= image_height:
        working_height = crop_height
    else:
        working_height = image_height - upper_left[0]
    if upper_left[1] + crop_width <= image_width:
        working_width = image_width
    else:
        working_width = image_width - upper_left[1]

    # Change one pixel at a time
    for row in range(working_height):
        for column in range(working_width):
                image[(upper_left[0]+row)][(upper_left[1]+column)] = piece[row][column]

# Calculate the average of each colour in the image
def average(image):
    image_height = len(image)
    image_width = len(image[0])

    colours_counters =[0]*RANGE_OF_COLOURS
    num_of_pixels = (image_width*image_height)
    # Run on all the pixels one colour at a time
    for c in range(RANGE_OF_COLOURS):
        for row in range(image_height):
            for column in range(image_width):
                colours_counters[c] += image[row][column][c]

    average_colours = [0]*RANGE_OF_COLOURS
    for c in range(RANGE_OF_COLOURS):
        average_colours[c] = (colours_counters[c]/num_of_pixels)
    result = tuple(average_colours)
    return result

# Calculate the avarage colours for each tile
def preprocess_tiles(tiles):

    # Create the empty list to be filled with averages
    result = [0]*len(tiles)
    #Calculate the average one at a time
    for i in range(len(tiles)):
        tile = tiles[i]
        result[i] = average(tile)
    return result

# Selecting the fitting tiles according to averages of the given tiles and the objective image
def get_best_tiles(objective, tiles, averages , num_candidates):
    image_avg = average(objective)
    result = [0]*num_candidates
    avg_dst_counters =[compare_pixel(image_avg,i) for i in averages]

    for i in range(num_candidates):
        # Index of the minimal distance
        j = avg_dst_counters.index(min(avg_dst_counters))
        result[i] = tiles[j]
        avg_dst_counters.remove(avg_dst_counters[j])

    #TODO: check perhaps we need a deep copy here
    return result


def choose_tile(piece, tiles):
    counters = [0]*len(tiles)

    # Set the counters
    for i in range(len(tiles)):
        counters[i] += compare(piece,tiles[i])
    #find the best fitting tile
    k = counters.index(min(counters))
    result = tiles[k]
    return result


def make_mosaic(image, tiles, num_candidates):
    # Set the working parameters
    image_height = len(image)
    image_width = len(image[0])
    tile_height = len(tiles[0])
    tile_width = len(tiles[0][0])
    size = (tile_height,tile_width)
    # Calculate tiles averages
    tiles_averages = preprocess_tiles(tiles)

    for row in range(0,image_height,tile_height):
        for column in range(0,image_width,tile_width):
            corner = (row,column)
            # Select a piece from the image
            piece = get_piece(image,corner,size)
            piece_average = average(piece)
            # Select the best fitting tile
            selected_tiles = get_best_tiles(piece,tiles,tiles_averages,num_candidates)
            most_fitting_tile = choose_tile(piece,selected_tiles)
            # Replace the image with the best tile
            set_piece(image,corner,most_fitting_tile)

# Writing the main function
def main():
    base = mosaic.build_tile_base(images_dir,tile_height)
    image = mosaic.load_image(image_source)
    final_image = make_mosaic(image,base,num_candidates)
    mosaic.show(final_image)
    mosaic.save(final_image,output_name)

if __name__ == '__main__':
    if len(sys.argv) == (NUMBER_OF_ARGUMENTS+1):
        script_name = sys.argv[0]
        image_source = sys.argv[1]
        images_dir = sys.argv[2]
        output_name = sys.argv[3]
        tile_height = int(sys.argv[4])
        num_candidates = int(sys.argv[5])
    else:
        # Printing error message
        print("wrong number of inputs: Please note the format is:\n"
              +"<image_src> <image_dir> <output_name> <tile_height> <num_candidates>")

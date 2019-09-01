import random
import time
import math
import matplotlib.pyplot as plt
import pdb


def time_it(func, *args):
    start = time.time()
    func(*args)
    end = time.time()
    return end - start


def euclidian_dist(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def evaluate(func):
    n_points = [10**k for k in range(1, 5)]
    times_taken = []
    for n in n_points:
        x0, xlim, y0, ylim = -200, 200, -200, 200
        points = create_random_points(x0, xlim, y0, ylim, n)
        start = time.time()
        dmin, closest_points = get_closest_points(points)
        end = time.time()
        times_taken.append(end - start)
    
    plt.scatter(list(range(1, 5)), [math.log10(duration*1000 + 1) for duration in times_taken], color = 'blue')
    plt.xlabel('number of points (powers of ten)')
    plt.ylabel('time taken (powers of ten) (ms)')
    plt.xticks(list(range(1,11)))
    plt.yticks([math.log10(duration*1000 + 1) for duration in times_taken])
    plt.show()


def draw(points, closest_points):
    plt.figure(figsize = (10, 8))
    plt.scatter([i[0] for i in points], [i[1] for i in points], color = 'blue')
    plt.scatter([closest_points[0][0], closest_points[1][0]], [closest_points[0][1], closest_points[1][1]], color = 'red')
    plt.show()


def create_random_points(x0, xlim, y0, ylim, n_points):
    points_list = []
    for i in range(n_points):
        point = (random.randint(x0, xlim), random.randint(y0, ylim))
        while point in points_list:
            point = (random.randint(x0, xlim), random.randint(y0, ylim))
        points_list.append(point)

    return points_list


def get_closest_points(points):
    len_points = len(points)

    if len_points == 0 or len_points == 1:
        print('empty set of points')
        return
    
    elif len_points == 2:
        return euclidian_dist(points[0], points[1]), points

    # Sort points based on their x values.
    x_sorted_points = sorted(points, key = lambda x: x[0])
    return get_closest_points_internal(x_sorted_points)

def get_closest_points_internal(points):
    len_points = len(points)
    
    if len_points == 1:
        return [math.inf, points]
    if len_points == 2:
        return [math.sqrt((points[0][0] - points[1][0])**2 + (points[0][1] - points[1][1])**2), points]
    
    # dividing input to two halves
    first_half = points[:len_points//2]
    second_half = points[len_points//2:]

    # getting minimum distance between two points in each half
    d_f_min, f_closest_points = get_closest_points_internal(first_half)
    d_s_min, s_closest_points = get_closest_points_internal(second_half)

    # minimum distance in two halves
    d_fs_min = min(d_f_min, d_s_min)

    # getting minimum interdistance between halves
    min_inter_dist, closest_inter_points = interhalves_closest_points(d_fs_min, first_half, second_half) 
    
    # choosing the minimum distance with the corresponding point
    if min_inter_dist < d_fs_min:  
        return [min_inter_dist, closest_inter_points]
    elif d_f_min > d_s_min:
        return [d_s_min, s_closest_points]
    else:
        return [d_f_min, f_closest_points]
    

def interhalves_closest_points(d_fs_min, first_half, second_half):

    min_inter_dist = d_fs_min
    out_of_range = False
    i = len(first_half) - 1
    closest_inter_point = -1
    # calculate distance between points starting from closest ones on the x axis
    while i > -1 and not out_of_range:
        for j in range(len(second_half)):
            first_x = first_half[i][0]
            first_y = first_half[i][1]
            second_x = second_half[j][0]
            second_y = second_half[j][1]

            # if distance between x-values exceeds minimum distance 
            # then all points after this one will give bigger distance (because halves are sorted)    
            if abs(second_x - first_x) > d_fs_min:
                if j == 0:
                    out_of_range = True
                break
            
            dist_i_j = math.sqrt((first_x - second_x)**2 + (first_y - second_y)**2)
            if dist_i_j < min_inter_dist:
                min_inter_dist = dist_i_j
                closest_inter_point = [first_half[i], second_half[j]]
        i -= 1
    
    return min_inter_dist, closest_inter_point 


def brute_closest_point(points):
    dists = [[i for i in range(len(points))] for k in range(len(points))]
    min_dist = math.inf
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dists[i][j] = euclidian_dist(points[i], points[j])
            if dists[i][j] < min_dist:
                min_dist = dists[i][j]
                closest_point = [points[i], points[j]]
    return [min_dist, closest_point]    

def main():
    x0 = -200
    xlim = 200
    y0 = -100
    ylim = 100
    n_points = 50
    points = create_random_points(x0, xlim, y0, ylim, n_points)
    d, closest_points = get_closest_points(points)
    draw(points, closest_points)

if __name__ == '__main__':
    main()

        

    
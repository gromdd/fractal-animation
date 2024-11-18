import numpy as np
import matplotlib.pyplot as plt
import PIL
import imageio
import warnings
from fractal_point import *
from multiprocessing import Pool
warnings.filterwarnings("ignore")



def adjusted_point_on_line(frame_index, number_of_frames, end_of_line_space):
    normal_point_on_unit_line=frame_index/(number_of_frames-1)
    adjusted_point_on_unit_line=np.tan(np.pi/4*(normal_point_on_unit_line*2-1))/2+1/2
    return end_of_line_space+adjusted_point_on_unit_line*(1-2*end_of_line_space)


def normal_point_on_line(frame_index, number_of_frames, end_of_line_space):
    normal_point_on_unit_line=frame_index/(number_of_frames-1)
    return end_of_line_space+normal_point_on_unit_line*(1-2*end_of_line_space)   


    
number_of_worker_threads=4

number_of_frames=501

fps=20

end_of_line_space=1/10

animation_name="Levy_C_curve_animation"

starting_line=[point(0, 0), point(1, 0)]

starting_line=starting_line

alternating=1

change_alternation=1

tol=2*10**(-3)

max_iter=500

point_on_line=adjusted_point_on_line

transformation_step_dragon_curve = lambda frame_index: [point(0, 0),
                    point(0.5+0.5*np.cos(point_on_line(frame_index, number_of_frames, end_of_line_space)*np.pi),
                    0.5*np.sin(point_on_line(frame_index, number_of_frames, end_of_line_space)*np.pi)),
                    point(1, 0)]

transformation_step_sierpinski_triangle = lambda frame_index: [ point(0,0),
                    point(0.5+0.5*np.cos(np.pi-point_on_line(frame_index, number_of_frames, end_of_line_space)*np.pi),
                        0.5*np.sin(np.pi-point_on_line(frame_index, number_of_frames, end_of_line_space)*np.pi)  ),
                    point(0.5+0.5*np.cos(point_on_line(frame_index, number_of_frames, end_of_line_space)*np.pi),
                        0.5*np.sin(point_on_line(frame_index, number_of_frames, end_of_line_space)*np.pi)  ),
                    point(1,0)
                    ]

transformation_step=transformation_step_dragon_curve



def fractal_generator(starting_line, base_line_to_next_step, tol=10 ** (-3), max_iter=16, alternating=1, alternation_of_this=1, change_alternation=1):
    if((starting_line[1]-starting_line[0]).length() < tol or max_iter <= 0):
        return starting_line
    tmp = []
    vec_parallel = starting_line[1]-starting_line[0]
    vec_perpendicular = vec_parallel.rotation_90_deg()

    current_alternation = change_alternation*alternation_of_this if change_alternation==-1 else 1
    temporary_vector1 = starting_line[0]

    for point_i in base_line_to_next_step[1:]:
        temporary_vector2 = starting_line[0]+\
            vec_parallel * point_i.x+\
            vec_perpendicular*point_i.y*alternation_of_this

        tmp += fractal_generator([temporary_vector1, temporary_vector2],
                                 base_line_to_next_step,
                                 tol=tol,
                                 max_iter=max_iter-1,
                                 alternating=alternating,
                                 alternation_of_this=current_alternation,
                                 change_alternation=change_alternation)[:-1]

        current_alternation = alternating*current_alternation
        temporary_vector1 = temporary_vector2
    tmp.append(starting_line[1])
    return tmp



def image_generator(frame_index, starting_line, transformation_step, alternating=-1, max_iter=500, tol=2*10**(-3), change_alternation=1, s=[0.01]):
    fig = plt.figure(figsize=(19.2, 10.8))
    plt.axis("off")
    point_list = fractal_generator(
        starting_line,
        transformation_step,
        alternating=alternating,
        max_iter=max_iter,
        tol=tol,
        change_alternation=change_alternation
        )
    
    plt.scatter([i.x for i in point_list], [i.y for i in point_list],s=s)
    #plt.plot([i.x for i in point_list], [i.y for i in point_list])
    fig.canvas.draw()
    image = PIL.Image.frombytes('RGB',
        fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
    plt.close()
    
    return (image, frame_index)


def image_saver(image, file_name="image.png"):
    image.save(file_name)
    


def imap_wrapper(index):
    return image_generator(index, 
                starting_line,
                transformation_step(index),
                alternating=alternating,
                max_iter=max_iter,
                tol=tol,
                change_alternation=change_alternation
            )




'''
image_saver(image_generator(0,
                            starting_line,
                                [point(0, 0),
                                point(0.5+0.5*np.cos( end_of_line_space*np.pi),
                                0.5*np.sin( end_of_line_space*np.pi)),
                                point(1, 0)],
                            tol=4*10 ** (-3),
                            max_iter=500,
                            alternating=-1,
                            change_alternation=1,
                            s=[0.01])[0]
        , file_name="readme_image.png")

'''
if __name__=="__main__":
    

    writer = imageio.get_writer(animation_name+'.mp4', fps=fps, macro_block_size=8)

    with Pool(number_of_worker_threads) as p:
        
        for image, frame_index in p.imap(imap_wrapper,range(number_of_frames)):
            print("frame {} of {} done".format(frame_index+1, number_of_frames), end="\r")
            writer.append_data(np.array(image))
            
    writer.close()
    

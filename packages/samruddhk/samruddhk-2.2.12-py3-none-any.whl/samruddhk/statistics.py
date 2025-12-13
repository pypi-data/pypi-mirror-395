# import inspect

# # ===================== 📦 ML and Visualization Programs ===================== #
# """
# def program1():
#     % Read and display a digital image
#     img = imread('filepath/filename.jpg');
#     imshow(img);





# def program2():
#     % 2. Read multiple images and write to output folder
#     input_path  = 'C:\Users\...\cp0\';
#     output_path = 'C:\Users\...\outputs\';

#     for k = 1:5
#         img = imread([input_path num2str(k) '.jpg']);
#         imwrite(img, [output_path num2str(k) '.jpg']);
#     end




# def program3():
#     % 3. Convert RGB → Gray → Binary and display

#     img = imread('C:\Users\...\family photo.jpg');

#     gray = rgb2gray(img);
#     binary = imbinarize(gray);

#     figure;
#     subplot(1,3,1); imshow(img);    title('RGB');
#     subplot(1,3,2); imshow(gray);   title('Gray');
#     subplot(1,3,3); imshow(binary); title('Binary');


# def program4():
#     % 4. Read image and plot histogram
#     img = imread('filepath/filename.jpg');

#     figure;
#     imshow(img);

#     figure;
#     imhist(img);
#     title('Histogram');


# def program5():
#     % 5. Split RGB channels and display
#     img = imread('C:\Users\...\family photo.jpg');

#     R = img(:,:,1);
#     G = img(:,:,2);
#     B = img(:,:,3);

#     figure;
#     subplot(2,2,1); imshow(img); title('Original');
#     subplot(2,2,2); imshow(R);   title('Red Channel');
#     subplot(2,2,3); imshow(G);   title('Green Channel');
#     subplot(2,2,4); imshow(B);   title('Blue Channel');


# def program6():
#     % 6. Split image into 4 quadrants and display
#     img = imread('C:\Users\...\cp0\1.jpg');

#     [rows, cols, ~] = size(img);
#     mid_r = floor(rows/2);
#     mid_c = floor(cols/2);

#     Q1 = img(1:mid_r,       1:mid_c,       :);
#     Q2 = img(1:mid_r,       mid_c+1:end,   :);
#     Q3 = img(mid_r+1:end,   1:mid_c,       :);
#     Q4 = img(mid_r+1:end,   mid_c+1:end,   :);

#     figure;
#     subplot(2,2,1); imshow(Q1); title('Top-Left (Up)');
#     subplot(2,2,2); imshow(Q2); title('Top-Right (Right)');
#     subplot(2,2,3); imshow(Q3); title('Bottom-Left (Left)');
#     subplot(2,2,4); imshow(Q4); title('Bottom-Right (Down)');



# """


# def programall():

# """

#     % Read and display a digital image
#     img = imread('filepath/filename.jpg');
#     imshow(img);





#     % 2. Read multiple images and write to output folder
#     input_path  = 'C:\Users\...\cp0\';
#     output_path = 'C:\Users\...\outputs\';

#     for k = 1:5
#         img = imread([input_path num2str(k) '.jpg']);
#         imwrite(img, [output_path num2str(k) '.jpg']);
#     end





#     % 3. Convert RGB → Gray → Binary and display

#     img = imread('C:\Users\...\family photo.jpg');

#     gray = rgb2gray(img);
#     binary = imbinarize(gray);

#     figure;
#     subplot(1,3,1); imshow(img);    title('RGB');
#     subplot(1,3,2); imshow(gray);   title('Gray');
#     subplot(1,3,3); imshow(binary); title('Binary');



#     % 4. Read image and plot histogram
#     img = imread('filepath/filename.jpg');

#     figure;
#     imshow(img);

#     figure;
#     imhist(img);
#     title('Histogram');



#     % 5. Split RGB channels and display
#     img = imread('C:\Users\...\family photo.jpg');

#     R = img(:,:,1);
#     G = img(:,:,2);
#     B = img(:,:,3);

#     figure;
#     subplot(2,2,1); imshow(img); title('Original');
#     subplot(2,2,2); imshow(R);   title('Red Channel');
#     subplot(2,2,3); imshow(G);   title('Green Channel');
#     subplot(2,2,4); imshow(B);   title('Blue Channel');



#     % 6. Split image into 4 quadrants and display
#     img = imread('C:\Users\...\cp0\1.jpg');

#     [rows, cols, ~] = size(img);
#     mid_r = floor(rows/2);
#     mid_c = floor(cols/2);

#     Q1 = img(1:mid_r,       1:mid_c,       :);
#     Q2 = img(1:mid_r,       mid_c+1:end,   :);
#     Q3 = img(mid_r+1:end,   1:mid_c,       :);
#     Q4 = img(mid_r+1:end,   mid_c+1:end,   :);

#     figure;
#     subplot(2,2,1); imshow(Q1); title('Top-Left (Up)');
#     subplot(2,2,2); imshow(Q2); title('Top-Right (Right)');
#     subplot(2,2,3); imshow(Q3); title('Bottom-Left (Left)');
#     subplot(2,2,4); imshow(Q4); title('Bottom-Right (Down)');

    
# """
# # ===================== 🔍 Source Code Introspection Functions ===================== #

# # def print_program1(): print(inspect.getsource(program1))
# # def print_program2(): print(inspect.getsource(program2))
# # def print_program3(): print(inspect.getsource(program3))
# # def print_program4(): print(inspect.getsource(program4))
# # def print_program5(): print(inspect.getsource(program5))
# # def print_program6(): print(inspect.getsource(program6))
# def print_programall(): print(inspect.getsource(programall))


import inspect

# ============================================================
# MATLAB PROGRAM STRINGS
# ============================================================

program1 = """
% Program 1: Read and display image
img = imread('filepath/filename.jpg');
imshow(img);
"""

program2 = """
% Program 2: Read multiple images and write to output folder
input_path  = 'C:\\Users\\...\\cp0\\';
output_path = 'C:\\Users\\...\\outputs\\';

for k = 1:5
    img = imread([input_path num2str(k) '.jpg']);
    imwrite(img, [output_path num2str(k) '.jpg']);
end
"""

program3 = """
% Program 3: Convert RGB → Gray → Binary and display
img = imread('C:\\Users\\...\\family photo.jpg');

gray = rgb2gray(img);
binary = imbinarize(gray);

figure;
subplot(1,3,1); imshow(img);    title('RGB');
subplot(1,3,2); imshow(gray);   title('Gray');
subplot(1,3,3); imshow(binary); title('Binary');
"""

program4 = """
% Program 4: Read image and plot histogram
img = imread('filepath/filename.jpg');

figure;
imshow(img);

figure;
imhist(img);
title('Histogram');
"""

program5 = """
% Program 5: Split RGB channels and display
img = imread('C:\\Users\\...\\family photo.jpg');

R = img(:,:,1);
G = img(:,:,2);
B = img(:,:,3);

figure;
subplot(2,2,1); imshow(img); title('Original');
subplot(2,2,2); imshow(R);   title('Red Channel');
subplot(2,2,3); imshow(G);   title('Green Channel');
subplot(2,2,4); imshow(B);   title('Blue Channel');
"""

program6 = """
% Program 6: Split image into four quadrants
img = imread('C:\\Users\\...\\cp0\\1.jpg');

[rows, cols, ~] = size(img);
mid_r = floor(rows/2);
mid_c = floor(cols/2);

Q1 = img(1:mid_r,       1:mid_c,       :);
Q2 = img(1:mid_r,       mid_c+1:end,   :);
Q3 = img(mid_r+1:end,   1:mid_c,       :);
Q4 = img(mid_r+1:end,   mid_c+1:end,   :);

figure;
subplot(2,2,1); imshow(Q1); title('Top-Left (Up)');
subplot(2,2,2); imshow(Q2); title('Top-Right (Right)');
subplot(2,2,3); imshow(Q3); title('Bottom-Left (Left)');
subplot(2,2,4); imshow(Q4); title('Bottom-Right (Down)');
"""

program_all = (
    program1
    + "\n\n"
    + program2
    + "\n\n"
    + program3
    + "\n\n"
    + program4
    + "\n\n"
    + program5
    + "\n\n"
    + program6
)


# ============================================================
# PRINT FUNCTIONS
# ============================================================

def print_program1():
    print(program1)

def print_program2():
    print(program2)

def print_program3():
    print(program3)

def print_program4():
    print(program4)

def print_program5():
    print(program5)

def print_program6():
    print(program6)

def print_programall():
    print(program_all)

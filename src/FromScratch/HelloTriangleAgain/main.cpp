#include<iostream>
#include<glad/glad.h>
#include<glfw/glfw3.h>
#include <iostream>
#include <string>
#include <assert.h>

//Local variables
static int WINDOW_WIEDHT = 800, WINDOW_HEIGHT = 800;

// Functions definitions
void framebuffer_size_callback(GLFWwindow* window, int widht, int height);
void processInput(GLFWwindow* window);
int setUpGeometryTriangleA();
int setUpShaderA();

// SHADERS
// Vertex Shader - written in GLSL (openGL Shading Language)
const GLchar *vertexShaderSource = R"glsl(
 #version 400
 layout (location = 0) in vec3 position;
 void main()
 {
	 gl_Position = vec4(position.x, position.y, position.z, 1.0);
 }
 )glsl";	

// Fragment Shader A - defines the color of each pixel - written in GLSL
const GLchar *fragmentShaderSourceA = R"glsl(
 #version 400
 out vec4 color;
 void main()
 {
	color = vec4(1.0f, 0.5f, 0.2f, 1.0f);
 }
 )glsl";
 // Fragment Shader B - defines the color of each pixel - written in GLSL
const GLchar *fragmentShaderSourceB = R"glsl(
 #version 400
 out vec4 color;
 void main()
 {
	color = vec4(0.0f, 0.0f, 0.0f, 1.0f);
 }
 )glsl";


// Funcitons implementations
void framebuffer_size_callback(GLFWwindow* window, int widht, int height) 
{
    glViewport(0, 0, widht, height);
}
void processInput(GLFWwindow* window) 
{
    if(glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS){
        glfwSetWindowShouldClose(window, true);
    }
}
int setUpGeometryTriangleA()
{
    float vertices[] = {
        0.0,  0.0, 0.0,
        0.5,  0.0, 0.0,
        0.25,  0.5, 0.0,  
    };

    GLuint VBO, VAO;
    glGenBuffers(1, &VBO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
    glGenVertexArrays(1, &VAO);
    glBindVertexArray(VAO);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), (GLvoid *)0);
    glEnableVertexAttribArray(0);

    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindVertexArray(0);
    return VAO;
}
int setUpGeometryTriangleB()
{
    float vertices[] = {
        0.0,  0.0, 0.0,
        -0.5,  0.0, 0.0,
        -0.25,  0.5, 0.0   
    };

    GLuint VBO, VAO;
    glGenBuffers(1, &VBO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
    glGenVertexArrays(1, &VAO);
    glBindVertexArray(VAO);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), (GLvoid *)0);
    glEnableVertexAttribArray(0);

    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindVertexArray(0);
    return VAO;
}
int setUpShaderA()
{
    // Vertex Shader being created at runtime
    GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
    glCompileShader(vertexShader);
    // this part of the code check if tere are any error in the shader
    GLint  success;
    GLchar infoLog[512];
    glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
    if(!success)
    {
        glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
    }

    // Fragment Shader being created at runtime 
    GLint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentShaderSourceA, NULL);
    glCompileShader(fragmentShader);
    glGetShaderiv(fragmentShader, GL_LINK_STATUS, &success);
    if(!success) 
    {
        glGetProgramInfoLog(fragmentShader, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n"
				  << infoLog << std::endl;
    }

    GLuint shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);
    glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
    // Checking linkage errors
    if(!success) {
        glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::PROGRAM::LINKING_FAILED\n"
				  << infoLog << std::endl;
    }
    glDeleteShader(vertexShader);
	glDeleteShader(fragmentShader);
    return shaderProgram;
}
int setUpShaderB()
{
    // Vertex Shader being created at runtime
    GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
    glCompileShader(vertexShader);
    // this part of the code check if tere are any error in the shader
    GLint  success;
    GLchar infoLog[512];
    glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
    if(!success)
    {
        glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
    }

    // Fragment Shader being created at runtime 
    GLint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentShaderSourceB, NULL);
    glCompileShader(fragmentShader);
    glGetShaderiv(fragmentShader, GL_LINK_STATUS, &success);
    if(!success) 
    {
        glGetProgramInfoLog(fragmentShader, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n"
				  << infoLog << std::endl;
    }

    GLuint shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);
    glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
    if(!success) {
        glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::PROGRAM::LINKING_FAILED\n"
				  << infoLog << std::endl;
    }
    glDeleteShader(vertexShader);
	glDeleteShader(fragmentShader);
    return shaderProgram;
}


int main() 
{
    //GLFW configuration
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    // creates the GLFW window
    GLFWwindow* window = glfwCreateWindow(WINDOW_WIEDHT, WINDOW_HEIGHT, "My pretty little window", NULL, NULL);
    // veifies if the window was created correctly
    if(window == NULL){
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    // verifies if
    if(!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)){
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }

    framebuffer_size_callback(window, WINDOW_WIEDHT, WINDOW_HEIGHT);
    GLuint shaderIdA = setUpShaderA();
    GLuint shaderIdB = setUpShaderB();
    GLuint VAO1 = setUpGeometryTriangleA();
    GLuint VAO2 = setUpGeometryTriangleB();
    GLuint colorLocA = glGetUniformLocation(shaderIdA, "inputColor");
    GLuint colorLocB = glGetUniformLocation(shaderIdB, "inputColor");

    // REDNERIDNG LOOP
    while(!glfwWindowShouldClose(window)){
        processInput(window);

        // redering commnds
        glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        glUseProgram(shaderIdA);
        glBindVertexArray(VAO1);
        glDrawArrays(GL_TRIANGLES, 0, 3);

        glUseProgram(shaderIdB);
        glBindVertexArray(VAO2);
        glDrawArrays(GL_TRIANGLES, 0, 3);

        // check call events and swap buffers
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteVertexArrays(1, &VAO1);
    glDeleteVertexArrays(1, &VAO2);
    glfwTerminate();
    return 0;
}
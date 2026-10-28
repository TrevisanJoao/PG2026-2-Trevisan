#include<iostream>
#include<string>
#include<assert.h>

#include<glad/glad.h>
#include<glfw/glfw3.h>

/*
// Shaders
// First Shader
#version version_number
in type in_variable_name;
in type in_variable_name;

out type out_variable_name;

uniform type uniform_name;

void main()
{
    //process input(s) and do some weird graphics stuff
    ...
    //output processes stuff to output variable
    out_v
    ariable_name = weird_stuff_we_processes
}
*/
int main() {
    int nrAttributes;
    glGetIntegerv(GL_MAX_VERTEX_ATTRIBS, &nrAttributes);
    std::cout << "Maximum nr of vertex attributes supported: " << nrAttributes << std::endl;
}
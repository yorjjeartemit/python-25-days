#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <stdio.h>
float wall[] = {
    -0.5f,-0.5f,0.0f,
     0.5f,-0.5f,0.0f,
     0.5f, 0.0f,0.0f,
    -0.5f, 0.0f,0.0f
};
unsigned int wallInd[]={0,1,2,2,3,0};

float roof[]={
    -0.6f,0.0f,0.0f,
     0.6f,0.0f,0.0f,
     0.0f,0.5f,0.0f
};
float door[]={
    -0.15f,-0.5f,0.0f,
     0.15f,-0.5f,0.0f,
     0.15f,-0.1f,0.0f,
    -0.15f,-0.1f,0.0f
};
unsigned int doorInd[]={0,1,2,2,3,0};
const char* vertexShaderSource="#version 330 core\nlayout(location=0) in vec3 aPos;\nvoid main(){gl_Position=vec4(aPos,1.0);}";
const char* fragmentShaderSourceWall="#version 330 core\nout vec4 FragColor;\nvoid main(){FragColor=vec4(0.0,0.0,1.0,1.0);}";
const char* fragmentShaderSourceRoof="#version 330 core\nout vec4 FragColor;\nvoid main(){FragColor=vec4(1.0,1.0,1.0,1.0);}"; 
const char* fragmentShaderSourceDoor="#version 330 core\nout vec4 FragColor;\nvoid main(){FragColor=vec4(0.55,0.27,0.07,1.0);}"; 

unsigned int compileShader(unsigned int type,const char*source) {
    unsigned int shader=glCreateShader(type);
    glShaderSource(shader,1,&source,NULL);
    glCompileShader(shader);
    return shader;
}
unsigned int createProgram(const char*fragSource) {
    unsigned int vert=compileShader(GL_VERTEX_SHADER,vertexShaderSource);
    unsigned int frag=compileShader(GL_FRAGMENT_SHADER,fragSource);
    unsigned int program=glCreateProgram();
    glAttachShader(program,vert);
    glAttachShader(program,frag);
    glLinkProgram(program);
    glDeleteShader(vert);
    glDeleteShader(frag);
    return program;
}
void drawShape(float*vertices,unsigned int*indices,int vCount,unsigned int VAO,unsigned int VBO,unsigned int EBO) {
    glBindVertexArray(VAO);
    glBindBuffer(GL_ARRAY_BUFFER,VBO);
    glBufferData(GL_ARRAY_BUFFER,sizeof(float)*vCount,vertices,GL_STATIC_DRAW);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER,sizeof(unsigned int)*6,indices,GL_STATIC_DRAW);
    glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,3*sizeof(float),(void*)0);
    glEnableVertexAttribArray(0);
    glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_INT,0);
}
int main() {
    if (!glfwInit()) return -1;
    GLFWwindow* win= glfwCreateWindow(800,600,"2D house", NULL,NULL);
    if (!win){glfwTerminate();return -1;}
    glfwMakeContextCurrent(win);
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        return -1;
    }

    unsigned int VAO,VBO,EBO;
    glGenVertexArrays(1,&VAO);
    glGenBuffers(1,&VBO);
    glGenBuffers(1,&EBO);

    unsigned int wallProgram=createProgram(fragmentShaderSourceWall);
    unsigned int roofProgram=createProgram(fragmentShaderSourceRoof);
    unsigned int doorProgram=createProgram(fragmentShaderSourceDoor);
    while (!glfwWindowShouldClose(win)) {
        glClearColor(0.2f,0.3f,0.3f,1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
        glUseProgram(wallProgram);
        drawShape(wall, wallInd, sizeof(wall)/sizeof(float),VAO,VBO,EBO);
        glUseProgram(roofProgram);
        glBindVertexArray(VAO);
        glBindBuffer(GL_ARRAY_BUFFER, VBO);
        glBufferData(GL_ARRAY_BUFFER, sizeof(roof), roof, GL_STATIC_DRAW);
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,3*sizeof(float),(void*)0);
        glEnableVertexAttribArray(0);
        glDrawArrays(GL_TRIANGLES,0,3);

        glUseProgram(doorProgram);
        drawShape(door,doorInd,sizeof(door)/sizeof(float),VAO,VBO,EBO);
        glfwSwapBuffers(win);
        glfwPollEvents();
    }
    glDeleteVertexArrays(1,&VAO);
    glDeleteBuffers(1,&VBO);
    glDeleteBuffers(1,&EBO);
    glfwTerminate();
    return 0;
}
package com.alyyousuf.rolle;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import android.opengl.GLES20;
import android.util.Log;

public class Shader {
	private int vertexShaderHandle;
	private int fragmentShaderHandle;
	private int programHandle;
	
    Shader(String vertexShader, String fragmentShader, String[] attrs) {
    	
		// Load in the vertex shader.
	    vertexShaderHandle = loadShader(vertexShader, GLES20.GL_VERTEX_SHADER);
	    
	    // Load in the fragment shader.
	    fragmentShaderHandle = loadShader(fragmentShader, GLES20.GL_FRAGMENT_SHADER);
	    
	    // Create a program object and store the handle to it.
	    programHandle = GLES20.glCreateProgram();
	     
	    if (programHandle != 0)
	    {
	        // Bind the vertex shader to the program.
	        GLES20.glAttachShader(programHandle, vertexShaderHandle);
	     
	        // Bind the fragment shader to the program.
	        GLES20.glAttachShader(programHandle, fragmentShaderHandle);
	     
	        // Bind attributes
	        for(int i = 0; i < attrs.length; i++)
	        	GLES20.glBindAttribLocation(programHandle, i, attrs[i]);
	     
	        // Link the two shaders together into a program.
	        GLES20.glLinkProgram(programHandle);
	     
	        // Get the link status.
	        final int[] linkStatus = new int[1];
	        GLES20.glGetProgramiv(programHandle, GLES20.GL_LINK_STATUS, linkStatus, 0);
	     
	        // If the link failed, delete the program.
	        if (linkStatus[0] == 0)
	        {
	            GLES20.glDeleteProgram(programHandle);
	            programHandle = 0;
	        }
	    }
	     
	    if (programHandle == 0)
	    {
	        throw new RuntimeException("Error creating program.");
	    }
	}
	
	private int loadShader(String file, int type) {
		StringBuilder shaderSource = new StringBuilder();
		try {
			BufferedReader reader = new BufferedReader(new InputStreamReader(this.getClass().getClassLoader().getResourceAsStream("res/raw/"+file+".txt")));
			String line;
			while((line  = reader.readLine()) != null) {
				shaderSource.append(line).append("\n");
			}
			reader.close();
		} catch (IOException e) {
			Log.d("test", "Could not read file."+file);
			System.exit(-1);
		}
		// Load in the shader.
	    int shaderHandle = GLES20.glCreateShader(type);
	     
        // Pass in the shader source.
        GLES20.glShaderSource(shaderHandle, shaderSource.toString());
     
        // Compile the shader.
        GLES20.glCompileShader(shaderHandle);
     
        // Get the compilation status.
        final int[] compileStatus = new int[1];
        GLES20.glGetShaderiv(shaderHandle, GLES20.GL_COMPILE_STATUS, compileStatus, 0);
     
        // If the compilation failed, delete the shader.
        if (compileStatus[0] == 0)
        {
            GLES20.glDeleteShader(shaderHandle);
            shaderHandle = 0;
        }
	     
	    if (shaderHandle == 0)
	    {
	        throw new RuntimeException("Error creating shader.");
	    }
	    
		return shaderHandle;
	}
	
	public int getProgramHandle() {
		return programHandle;
	}
	
	public void start() {
		GLES20.glUseProgram(programHandle);
	}
	
	public void stop() {
		GLES20.glUseProgram(0);
	}
}

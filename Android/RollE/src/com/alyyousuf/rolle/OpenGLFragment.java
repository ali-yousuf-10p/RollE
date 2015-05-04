package com.alyyousuf.rolle;

import android.app.ActivityManager;
import android.app.Fragment;
import android.content.Context;
import android.content.pm.ConfigurationInfo;
import android.opengl.GLSurfaceView;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioGroup;

public class OpenGLFragment extends Fragment {
	
	private GLSurfaceView mGLSurfaceView;
	private MyRenderer mRenderer;
	private RadioGroup FilterRadio;
	
	public OpenGLFragment() {
		mGLSurfaceView = null;
		mRenderer = null;
	}
	
	@Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		
		View rootView = inflater.inflate(R.layout.visual_fragment, container, false);
		FilterRadio = (RadioGroup)rootView.findViewById(R.id.filter_radiogroup);
		
        mGLSurfaceView = new GLSurfaceView(this.getActivity().getApplicationContext());
		((ViewGroup) rootView).addView(mGLSurfaceView, 0, new ViewGroup.LayoutParams(
                 ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
                 
		// Check if the system supports OpenGL ES 2.0.
        final ActivityManager activityManager = (ActivityManager) this.getActivity().getApplicationContext().getSystemService(Context.ACTIVITY_SERVICE);
        final ConfigurationInfo configurationInfo = activityManager.getDeviceConfigurationInfo();
        final boolean supportsEs2 = configurationInfo.reqGlEsVersion >= 0x20000;
        
        if (supportsEs2)
        {
            // Request an OpenGL ES 2.0 compatible context.
            mGLSurfaceView.setEGLContextClientVersion(2);
     
            // Set the renderer to our demo renderer, defined below.
            mRenderer = new MyRenderer();
            mGLSurfaceView.setRenderer(mRenderer);
        }
        else
        {
            // This is where you could create an OpenGL ES 1.x compatible
            // renderer if you wanted to support both ES 1 and ES 2.
            return null;
        }
        
        return rootView;
    }
	
    public void setAngleX(float angle) {
    	if(mRenderer != null)
    		mRenderer.setAngleX(angle);
    }
	
    public void setAngleY(float angle) {
    	if(mRenderer != null)
    		mRenderer.setAngleY(angle);
    }
	
    public void setAngleZ(float angle) {
    	if(mRenderer != null)
    		mRenderer.setAngleZ(angle);
    }

	public void setAngle(float[] n) {
    	if(mRenderer != null) {
    		int radioButtonID = FilterRadio.getCheckedRadioButtonId();
    		View radioButton = FilterRadio.findViewById(radioButtonID);
    		int k = FilterRadio.indexOfChild(radioButton)*3;
    		
    		setAngleX(n[0+k]);
    		setAngleY(n[1+k]);
    		setAngleZ(n[2+k]);
    	}
	}
}

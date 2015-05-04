package com.alyyousuf.rolle;

import android.app.Fragment;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;

/**
 * A placeholder fragment containing a simple view.
 */
public class PIDFragment extends Fragment {

	private EditText pText;
	private EditText iText;
	private EditText dText;
	private Button setBtn;
	private Button zeroPIDBtn;
	private MainActivity mainActivity;
	
    public PIDFragment(MainActivity activity) {
    	mainActivity = activity;
    }
    
    public void setP(String txt) {
    	pText.setText(txt);
    }
    
    public void setI(String txt) {
    	iText.setText(txt);
    }
    
    public void setD(String txt) {
    	dText.setText(txt);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.pid_fragment, container, false);

        pText = (EditText) rootView.findViewById(R.id.pText);
        iText = (EditText) rootView.findViewById(R.id.iText);
        dText = (EditText) rootView.findViewById(R.id.dText);
        
        setBtn = (Button) rootView.findViewById(R.id.setBtn);
        setBtn.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				try{
					float p = 0;
					float i = 0;
					float d = 0;
					
					if(pText.getText().toString().length() > 0)
						p = Float.parseFloat(pText.getText().toString());
					if(iText.getText().toString().length() > 0)
						i = Float.parseFloat(iText.getText().toString());
					if(dText.getText().toString().length() > 0)
						d = Float.parseFloat(dText.getText().toString());

					mainActivity.setPID(p,i,d);
				}catch(Exception e){
					Log.e("PID", "Error", e);
				}
			}
		});
        
        zeroPIDBtn = (Button) rootView.findViewById(R.id.zeroPIDbtn);
        zeroPIDBtn.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				try{
					mainActivity.setPID(0,0,0);
				}catch(Exception e){
					Log.e("PID", "Error", e);
				}
			}
		});
        return rootView;
    }
}
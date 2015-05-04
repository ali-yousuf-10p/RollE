package com.alyyousuf.rolle;

import java.io.IOException;
import java.io.InputStream;
import java.util.Locale;
import java.util.UUID;

import android.app.Activity;
import android.app.ActionBar;
import android.app.Fragment;
import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.support.v13.app.FragmentPagerAdapter;
import android.os.Bundle;
import android.support.v4.view.ViewPager;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;


public class MainActivity extends Activity implements ActionBar.TabListener {
	
	private static final int requestCode_blRequest = 1;
	private MainActivity thisActivity;

    Fragment[] fragmentList;
    SectionsPagerAdapter mSectionsPagerAdapter;
    ViewPager mViewPager;
    MenuItem btIcon;
    
    private BluetoothAdapter btAdapter = null;
    private BluetoothDevice btDevice = null;
    private BluetoothSocket btSocket = null;
    private boolean btConnected = false;
    private InputStream btInStream = null;
    private static final String btAddress = "20:13:06:24:02:72";
    private static final UUID btUUDID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        thisActivity = this;
        
        setContentView(R.layout.activity_main);

        // Set up the action bar.
        final ActionBar actionBar = getActionBar();
        actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_TABS);

        // Create the adapter that will return a fragment for each of the three
        // primary sections of the activity.
        mSectionsPagerAdapter = new SectionsPagerAdapter(getFragmentManager());
        fragmentList = new Fragment[mSectionsPagerAdapter.getCount()];
        // Set up the ViewPager with the sections adapter.
        mViewPager = (ViewPager) findViewById(R.id.pager);
        mViewPager.setAdapter(mSectionsPagerAdapter);

        // When swiping between different sections, select the corresponding
        // tab. We can also use ActionBar.Tab#select() to do this if we have
        // a reference to the Tab.
        mViewPager.setOnPageChangeListener(new ViewPager.SimpleOnPageChangeListener() {
            @Override
            public void onPageSelected(int position) {
                actionBar.setSelectedNavigationItem(position);
            }
        });

        // For each of the sections in the app, add a tab to the action bar.
        for (int i = 0; i < mSectionsPagerAdapter.getCount(); i++) {
            // Create a tab with text corresponding to the page title defined by
            // the adapter. Also specify this Activity object, which implements
            // the TabListener interface, as the callback (listener) for when
            // this tab is selected.
            actionBar.addTab(
                    actionBar.newTab()
                            .setText(mSectionsPagerAdapter.getPageTitle(i))
                            .setTabListener(this));
        }
        
        btAdapter = BluetoothAdapter.getDefaultAdapter();
        
        BroadcastReceiver mReceiver = new BroadcastReceiver() {

			@Override
			public void onReceive(Context context, Intent intent) {
				final String action = intent.getAction();
				
				// Action State
				if (action.equals(BluetoothAdapter.ACTION_STATE_CHANGED)) {
		            final int state = intent.getIntExtra(BluetoothAdapter.EXTRA_STATE, BluetoothAdapter.ERROR);
		            
		            switch (state) {
		            case BluetoothAdapter.STATE_OFF:
		            	btDisconnect();
		                break;
		            }
		        }
				
				// Connection State
				if (action.equals(BluetoothDevice.ACTION_ACL_DISCONNECTED)) {
					if(btAdapter.isEnabled()) {
						Toast.makeText(getApplicationContext(), "Connection lost. Please reconnect.", Toast.LENGTH_SHORT).show();
						btDisconnect();
					}
		        }
			}
        };
        
        Runnable btReceiving = new Runnable() {

			@Override
			public void run() {
				while(true) {
					String message = "";
					while(btConnected && btInStream != null) {
						try {
							char ch = (char)btInStream.read();
							if(ch == '\n')
								break;
							message += ch;
						} catch (IOException e) {
							//Log.e("Bluetooth", "Exception during read.", e);
						}
					}
					
					if(message.startsWith("a:")) {
						String m[] = message.substring(2).split(",");
						if(m.length == 9) {
							final float n[] = {Float.parseFloat(m[0]), Float.parseFloat(m[1]), Float.parseFloat(m[2]), Float.parseFloat(m[3]), Float.parseFloat(m[4]), Float.parseFloat(m[5]), Float.parseFloat(m[6]), Float.parseFloat(m[7]), Float.parseFloat(m[8])};
							runOnUiThread(new Runnable() {

								@Override
								public void run() {
									if(paused) return;
									
									OpenGLFragment frag = (OpenGLFragment)fragmentList[0];
									if(frag != null) {
										frag.setAngle(n);
									}
								}
								
							});
							
						}
					}else if(message.startsWith("PID:")) {
						//Toast.makeText(getApplicationContext(), "Received something.", Toast.LENGTH_SHORT).show();
						Log.d("PID", message);
						final String m[] = message.substring(4).split(",");
						if(m.length == 3) {
							//final float n[] = {Float.parseFloat(m[0]), Float.parseFloat(m[1]), Float.parseFloat(m[2])};
							
							runOnUiThread(new Runnable() {

								@Override
								public void run() {
									EditText pText = (EditText) findViewById(R.id.pText);
									EditText iText = (EditText) findViewById(R.id.iText);
									EditText dText = (EditText) findViewById(R.id.dText);

									pText.setText(m[0]);
									iText.setText(m[1]);
									dText.setText(m[2]);
									
									Toast.makeText(getApplicationContext(), "Received current PID values from the robot.", Toast.LENGTH_SHORT).show();
								}
								
							});
						}
					}
				}
			}
        	
        };
        Thread btReceivingThread = new Thread(btReceiving);
        btReceivingThread.start();
        
        IntentFilter filter = new IntentFilter(BluetoothAdapter.ACTION_STATE_CHANGED);
        filter.addAction(BluetoothDevice.ACTION_ACL_DISCONNECTED);
        registerReceiver(mReceiver, filter);
    }
    
    public void btDisconnect() {
    	if(!btConnected) return;	// Prevent double calls
    	
    	try {
    		if(btSocket != null)
    			btSocket.close();
    	} catch(Exception e) {
    		// Do nothing
    	}
    	btSocket = null;
		btConnected = false;
		btIcon.setIcon(R.drawable.bluetooth_connect);
    	Toast.makeText(getApplicationContext(), "RollE disconnected.", Toast.LENGTH_SHORT).show();
    }
    
    public boolean btEnable() {
    	if(btAdapter.isEnabled() == false) {
    		btDisconnect();
    		Intent btTurnOnIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
    		startActivityForResult(btTurnOnIntent, requestCode_blRequest);
    		return false;
    	}
    	return true;
    }
    
    public void btConnect() {
    	if(!btEnable())
    		return;
    	if(btSocket != null && btSocket.isConnected())
    		return;
    	
    	btDevice = btAdapter.getRemoteDevice(btAddress);
    	
    	try {
    		btSocket = btDevice.createRfcommSocketToServiceRecord(btUUDID);
    	} catch(IOException e) {
    		Log.e("Bluetooth", "Socket creation failed", e);
    	}
    	
    	btAdapter.cancelDiscovery();
    	
    	try {
    		btSocket.connect();
    	} catch (IOException e) {
            try {
                btSocket.close();
	        } catch (IOException e2) {
	                Log.e("Bluetooth", "Unable to close socket during connection failure", e2);
	        }
            return;
    	}
    	
    	btConnected = true;
		btIcon.setIcon(R.drawable.bluetooth_connected);
    	Toast.makeText(getApplicationContext(), "RollE connected.", Toast.LENGTH_SHORT).show();
    	
    	try {
    		btInStream = btSocket.getInputStream();
    	} catch (IOException e) {
    		btSocket = null;
			Log.e("Bluetooth", "Exception in creating InputStream.", e);
    	}
    	
    	String message = "PID?\n";
    	try {
			btSocket.getOutputStream().write(message.getBytes());
		} catch (IOException e) {
			btSocket = null;
			Log.e("Bluetooth", "Exception during write.", e);
		}
    }
    
    boolean paused = true;
    @Override
    public void onResume() {
    	super.onResume();
    	paused = false;
    }
    
    @Override
    public void onPause() {
    	super.onPause();
    	paused = true;
    }
    
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
    	if(requestCode == requestCode_blRequest) {
    		if(btAdapter.isEnabled())
    			btConnect();
    			//Toast.makeText(getApplicationContext(), "Bluetooth turned on.", Toast.LENGTH_SHORT).show();
    	}
    }
    
    public void setPID(float P, float I, float D) {
    	if(!btConnected) return;
    	
    	try {
    		String message = String.format("PID:%.2f,%.2f,%.2f", P, I, D);

    		Log.d("Bluetooth", message);
			btSocket.getOutputStream().write(message.getBytes());
		} catch (Exception e) {
			btSocket = null;
			Log.e("Bluetooth", "Exception during write.", e);
		}
    }
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        btIcon = menu.getItem(0);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_bluetooth) {
        	if(btConnected) {
        		btDisconnect();
        	}else{
        		btConnect();
        	}
        }
        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onTabSelected(ActionBar.Tab tab, FragmentTransaction fragmentTransaction) {
        // When the given tab is selected, switch to the corresponding page in
        // the ViewPager.
        mViewPager.setCurrentItem(tab.getPosition());
    }

    @Override
    public void onTabUnselected(ActionBar.Tab tab, FragmentTransaction fragmentTransaction) {
    }

    @Override
    public void onTabReselected(ActionBar.Tab tab, FragmentTransaction fragmentTransaction) {
    }

    public class SectionsPagerAdapter extends FragmentPagerAdapter {

        public SectionsPagerAdapter(FragmentManager fm) {
            super(fm);
        }

        @Override
        public Fragment getItem(int position) {
        	if(position == 0)
        		fragmentList[position] = new OpenGLFragment();
        	else
            	fragmentList[position] = new PIDFragment(thisActivity);

            return fragmentList[position];
        }

        @Override
        public int getCount() {
            // Show 2 total pages.
            return 2;
        }

        @Override
        public CharSequence getPageTitle(int position) {
            Locale l = Locale.getDefault();
            switch (position) {
                case 0:
                    return getString(R.string.title_section1).toUpperCase(l);
                case 1:
                    return getString(R.string.title_section2).toUpperCase(l);
            }
            return null;
        }
    }

}

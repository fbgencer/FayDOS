package com.example.myapplication;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.net.wifi.p2p.WifiP2pManager;
import android.widget.Toast;

public class WiFiDirectBroadcastReceiver extends BroadcastReceiver {
    private WifiP2pManager mp2p;
    private WifiP2pManager.Channel mch;
    private MainActivity mActivity;

    public WiFiDirectBroadcastReceiver(WifiP2pManager mp2p, WifiP2pManager.Channel mch, MainActivity mActivity){
        this.mp2p = mp2p;
        this.mch = mch;
        this.mActivity = mActivity;
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        String action = intent.getAction();
        if(WifiP2pManager.WIFI_P2P_STATE_CHANGED_ACTION.equals(action)){
            int state = intent.getIntExtra(WifiP2pManager.EXTRA_WIFI_STATE,-1);
            if(state == WifiP2pManager.WIFI_P2P_STATE_ENABLED){
                Toast.makeText(context,"WiFi is ON", Toast.LENGTH_SHORT).show();
            }
            else{
                Toast.makeText(context,"WiFi is OFF", Toast.LENGTH_SHORT).show();
            }

        } else if (WifiP2pManager.WIFI_P2P_PEERS_CHANGED_ACTION.equals(action)) {
            if(mp2p != null){
                mp2p.requestPeers(mch,mActivity.peerListListener);
            }
        }
        else if(WifiP2pManager.WIFI_P2P_CONNECTION_CHANGED_ACTION.equals(action)){

        }
        else if(WifiP2pManager.WIFI_P2P_THIS_DEVICE_CHANGED_ACTION.equals(action)){

        }
    }
}

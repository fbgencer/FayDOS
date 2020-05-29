package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.IntentFilter;
import android.net.wifi.WifiManager;
import android.net.wifi.p2p.WifiP2pDevice;
import android.net.wifi.p2p.WifiP2pDeviceList;
import android.net.wifi.p2p.WifiP2pManager;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity{
    Button btnWiFiOn, btnScan, btnSend;
    TextView conStatus;
    EditText messageText;
    ListView lView;

    WifiManager wf;
    WifiP2pManager mp2p;
    WifiP2pManager.Channel mch;

    BroadcastReceiver mBReceiver;
    IntentFilter iFilter;

    List<WifiP2pDevice> peers = new ArrayList<WifiP2pDevice>();
    String[] devNameArray;
    WifiP2pDevice [] devArray;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initialize();
        initListeners();
    }

    private void initialize(){
        btnWiFiOn = findViewById(R.id.buttonWiFiOn);
        btnScan = findViewById(R.id.buttonScan);
        btnSend = findViewById(R.id.buttonSend);
        btnSend.setVisibility(View.INVISIBLE);

        conStatus = findViewById(R.id.connectionStatus);

        lView = findViewById(R.id.peerDeviceList);

        messageText = findViewById(R.id.messageText);
        messageText.setVisibility(View.INVISIBLE);

        wf = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);

        mp2p =(WifiP2pManager) getSystemService(Context.WIFI_P2P_SERVICE);
        mch = mp2p.initialize(this,getMainLooper(),null);

        mBReceiver = new WiFiDirectBroadcastReceiver(mp2p,mch,this);
        iFilter = new IntentFilter();
        iFilter.addAction(WifiP2pManager.WIFI_P2P_STATE_CHANGED_ACTION);
        iFilter.addAction(WifiP2pManager.WIFI_P2P_PEERS_CHANGED_ACTION);
        iFilter.addAction(WifiP2pManager.WIFI_P2P_CONNECTION_CHANGED_ACTION);
        iFilter.addAction(WifiP2pManager.WIFI_P2P_THIS_DEVICE_CHANGED_ACTION);

    }

    WifiP2pManager.PeerListListener peerListListener = new WifiP2pManager.PeerListListener() {
        @Override
        public void onPeersAvailable(WifiP2pDeviceList incPeers) {
            if(!incPeers.getDeviceList().equals(peers)){
                peers.clear();
                peers.addAll(incPeers.getDeviceList());

                devNameArray = new String[incPeers.getDeviceList().size()];
                devArray = new WifiP2pDevice[incPeers.getDeviceList().size()];

                int index = 0;
                for(WifiP2pDevice dv : incPeers.getDeviceList()){
                    devNameArray[index] = dv.deviceName;
                    devArray[index] = dv;
                    ++index;
                }
                ArrayAdapter<String> adapter = new ArrayAdapter<String>( getApplicationContext(),android.R.layout.simple_list_item_1,devNameArray);
                lView.setAdapter(adapter);

                if(peers.size() == 0){
                    Toast.makeText(getApplicationContext(), "No Device Found", Toast.LENGTH_SHORT).show();
                }
            }
        }
    };

    @Override
    protected void onResume() {
        super.onResume();
        registerReceiver(mBReceiver,iFilter);
    }

    @Override
    protected void onPause() {
        super.onPause();
        unregisterReceiver(mBReceiver);
    }

    private void initListeners(){
        btnWiFiOn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(wf.isWifiEnabled()){
                    wf.setWifiEnabled(false);
                    btnWiFiOn.setText(R.string.buttonWiFiOn);
                    //Toast.makeText(getApplicationContext(), "WiFi Closed", Toast.LENGTH_SHORT).show();
                }
                else{
                    wf.setWifiEnabled(true);
                    btnWiFiOn.setText(R.string.buttonWiFiOff);
                    //Toast.makeText(getApplicationContext(), "WiFi Opened", Toast.LENGTH_SHORT).show();
                }

            }
        });
        btnScan.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mp2p.discoverPeers(mch, new WifiP2pManager.ActionListener() {
                    @Override
                    public void onSuccess() {
                        conStatus.setText("Discovery Started");
                    }

                    @Override
                    public void onFailure(int reason) {
                        conStatus.setText("Discovery Start Failed");
                    }
                });
            }
        });
    }




}

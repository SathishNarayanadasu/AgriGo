package com.agrigo.activities;

import android.content.Context;
import android.os.Bundle;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import com.agrigo.utils.LocaleHelper;

public class BaseActivity extends AppCompatActivity {

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Keep screen on while using the app to prevent OS from killing it
        getWindow().addFlags(android.view.WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        // Do not replace Android's process-wide uncaught-exception handler from
        // every Activity. Calling System.exit() here can kill the whole process
        // during a transient background error and looks like an unexpected logout.
    }

    @Override
    protected void attachBaseContext(Context newBase) {
        try {
            super.attachBaseContext(LocaleHelper.onAttach(newBase));
        } catch (Exception e) {
            android.util.Log.e("BaseActivity", "Failed to attach locale context", e);
            super.attachBaseContext(newBase);
        }
    }

    @Override
    public void onConfigurationChanged(android.content.res.Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
        try {
            LocaleHelper.onAttach(this);
        } catch (Exception e) {
            android.util.Log.e("BaseActivity", "Failed to update locale", e);
        }
    }
}

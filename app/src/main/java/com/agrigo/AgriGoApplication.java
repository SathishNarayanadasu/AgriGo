package com.agrigo;

import android.app.Application;
import timber.log.Timber;

/**
 * AgriGo Application class.
 * Initializes global libraries like Timber for logging.
 */
public class AgriGoApplication extends Application {

    @Override
    public void onCreate() {
        super.onCreate();

        // Initialize Timber for debug logging
        if (BuildConfig.DEBUG) {
            Timber.plant(new Timber.DebugTree());
        }
    }
}

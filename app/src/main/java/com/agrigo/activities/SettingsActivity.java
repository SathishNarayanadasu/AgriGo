package com.agrigo.activities;

import android.os.Bundle;
import android.widget.ImageButton;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import com.agrigo.R;

public class SettingsActivity extends BaseActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        
        findViewById(R.id.btnBack).setOnClickListener(v -> finish());
        ((TextView)findViewById(R.id.tvTitle)).setText("Settings");
        
        findViewById(R.id.layoutLanguage).setOnClickListener(v -> showLanguageDialog());
    }

    private void showLanguageDialog() {
        String[] languages = {"English", "తెలుగు (Telugu)"};
        final String[] langCodes = {"en", "te"};
        int checkedItem = com.agrigo.utils.LocaleHelper.getLanguage(this).equals("te") ? 1 : 0;
        final int[] selected = {checkedItem};

        new androidx.appcompat.app.AlertDialog.Builder(this)
                .setTitle(getString(R.string.language_label))
                .setSingleChoiceItems(languages, checkedItem, (dialog, which) -> {
                    selected[0] = which;
                })
                .setPositiveButton(R.string.save, (dialog, which) -> {
                    String langCode = langCodes[selected[0]];
                    com.agrigo.utils.LocaleHelper.setLocale(this, langCode);
                    dialog.dismiss();
                })
                .setNegativeButton(R.string.cancel, null)
                .show();
    }
}

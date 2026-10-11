package com.users.ffq_app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import com.users.ffq_app.data.local.AppPrefs
import com.users.ffq_app.ui.navigation.AppNavigator
import com.users.ffq_app.ui.theme.FFQAppTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            var themeMode by remember { mutableStateOf(AppPrefs.getThemeMode(this)) }
            FFQAppTheme(themeMode = themeMode) {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    AppNavigator(
                        themeMode = themeMode,
                        onThemeModeChanged = { themeMode = it }
                    )
                }
            }
        }
    }
}

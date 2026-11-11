package com.users.ffq_app.ui.navigation

import android.app.Activity
import android.widget.Toast
import androidx.activity.compose.BackHandler
import androidx.compose.animation.Crossfade
import androidx.compose.animation.core.tween
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.unit.LayoutDirection
import com.users.ffq_app.data.model.AppStrings
import com.users.ffq_app.data.model.LocalAppStrings
import com.users.ffq_app.data.model.PatientRecord
import com.users.ffq_app.data.model.RegistrationData
import com.users.ffq_app.ui.screens.*
import com.users.ffq_app.util.FFQRepository
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

@Composable
fun AppNavigator(
    themeMode: String = "light",
    onThemeModeChanged: (String) -> Unit = {}
) {
    var currentScreen: Screen by remember { mutableStateOf(Screen.Splash) }
    val activity = (LocalContext.current as? Activity)
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var backPressedOnce by remember { mutableStateOf(false) }

    // Persian RTL Layout
    CompositionLocalProvider(
        LocalLayoutDirection provides LayoutDirection.Rtl,
        LocalAppStrings provides AppStrings()
    ) {
        val strings = LocalAppStrings.current

        BackHandler {
            when (currentScreen) {
                is Screen.Splash -> { }
                is Screen.Login -> activity?.finish()
                is Screen.AdminLogin -> currentScreen = Screen.Login
                is Screen.AdminDashboard -> currentScreen = Screen.Login
                is Screen.MainMenu -> {
                    if (backPressedOnce) {
                        activity?.finish()
                    } else {
                        backPressedOnce = true
                        Toast.makeText(context, strings.pressBackAgain, Toast.LENGTH_SHORT).show()
                        scope.launch {
                            delay(2000)
                            backPressedOnce = false
                        }
                    }
                }
                is Screen.Registration -> currentScreen = Screen.MainMenu
                is Screen.FFQQuestionnaire -> currentScreen = Screen.MainMenu
                is Screen.History -> currentScreen = Screen.MainMenu
                is Screen.PatientDetail -> currentScreen = Screen.History
                is Screen.ContactUs -> currentScreen = Screen.MainMenu
                is Screen.Settings -> currentScreen = Screen.MainMenu
            }
        }

        Crossfade(targetState = currentScreen, animationSpec = tween(400), label = "screen_transition") { screen ->
            when (screen) {
                is Screen.Splash -> SplashScreen(onFinished = { currentScreen = Screen.Login })
                is Screen.Login -> LoginScreen(
                    onLoginSuccess = { currentScreen = Screen.MainMenu },
                    onAdminClick = { currentScreen = Screen.AdminLogin }
                )
                is Screen.AdminLogin -> AdminLoginScreen(
                    onSuccess = { currentScreen = Screen.AdminDashboard },
                    onBack = { currentScreen = Screen.Login }
                )
                is Screen.AdminDashboard -> AdminDashboardScreen(
                    onBack = { currentScreen = Screen.Login },
                    onThemeModeChanged = onThemeModeChanged
                )
                is Screen.MainMenu -> MainMenuScreen(
                    onNavigate = { currentScreen = it },
                    onExitApp = { activity?.finish() },
                    onLogout = { currentScreen = Screen.Login }
                )
                is Screen.Registration -> RegistrationScreen(
                    initialData = screen.initialData,
                    onNavigateBack = { currentScreen = Screen.MainMenu },
                    onProceedToFFQ = { regData ->
                        currentScreen = Screen.FFQQuestionnaire(patientId = regData.id, registrationData = regData)
                    }
                )
                is Screen.FFQQuestionnaire -> {
                    val existing = FFQRepository.getRecord(context, screen.patientId)
                    FFQQuestionnaireScreen(
                        patientId = screen.patientId,
                        registrationData = screen.registrationData,
                        initialAnswers = existing?.answers ?: emptyMap(),
                        onNavigateBack = { currentScreen = Screen.MainMenu },
                        onSaveSuccess = { currentScreen = Screen.PatientDetail(screen.patientId) }
                    )
                }
                is Screen.History -> HistoryScreen(
                    onPatientSelected = { id -> currentScreen = Screen.PatientDetail(id) },
                    onNavigateBack = { currentScreen = Screen.MainMenu }
                )
                is Screen.PatientDetail -> PatientDetailScreen(
                    patientId = screen.patientId,
                    onNavigateBack = { currentScreen = Screen.History },
                    onEditRegistration = { reg ->
                        currentScreen = Screen.Registration(initialData = reg)
                    },
                    onOpenFFQ = { record ->
                        currentScreen = Screen.FFQQuestionnaire(patientId = record.patientId, registrationData = record.registration)
                    }
                )
                is Screen.ContactUs -> ContactUsScreen(onNavigateBack = { currentScreen = Screen.MainMenu })
                is Screen.Settings -> ContactUsScreen(onNavigateBack = { currentScreen = Screen.MainMenu })
            }
        }
    }
}

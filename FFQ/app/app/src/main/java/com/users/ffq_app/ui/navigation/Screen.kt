package com.users.ffq_app.ui.navigation

import com.users.ffq_app.data.model.RegistrationData

sealed class Screen {
    data object Splash : Screen()
    data object Login : Screen()
    data object AdminLogin : Screen()
    data object AdminDashboard : Screen()
    data object MainMenu : Screen()
    data class Registration(val initialData: RegistrationData? = null) : Screen()
    data class FFQQuestionnaire(val patientId: String, val registrationData: RegistrationData) : Screen()
    data object History : Screen()
    data class PatientDetail(val patientId: String) : Screen()
    data object ContactUs : Screen()
    data object Settings : Screen()
}

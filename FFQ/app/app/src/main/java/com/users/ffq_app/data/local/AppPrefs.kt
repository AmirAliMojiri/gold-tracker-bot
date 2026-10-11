package com.users.ffq_app.data.local

import android.content.Context
import androidx.core.content.edit
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken

object AppPrefs {
    private const val PREFS_NAME = "FFQPrefs"
    private fun getPrefs(context: Context) = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    fun getUsers(context: Context): List<Pair<String, String>> {
        val json = getPrefs(context).getString("allowed_users", null)
        if (json == null) {
            // Default initial user
            val initial = listOf("user" to "1234")
            saveUsers(context, initial)
            return initial
        }
        val type = object : TypeToken<List<Pair<String, String>>>() {}.type
        return try {
            Gson().fromJson(json, type) ?: emptyList()
        } catch (e: Exception) {
            emptyList()
        }
    }

    fun saveUsers(context: Context, users: List<Pair<String, String>>) {
        getPrefs(context).edit { putString("allowed_users", Gson().toJson(users)) }
    }

    // Theme Mode: "light", "dark", "system"
    fun getThemeMode(context: Context): String {
        return getPrefs(context).getString("app_theme_mode", "light") ?: "light"
    }

    fun setThemeMode(context: Context, mode: String) {
        getPrefs(context).edit { putString("app_theme_mode", mode) }
    }
}

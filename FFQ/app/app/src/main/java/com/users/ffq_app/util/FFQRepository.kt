package com.users.ffq_app.util

import android.content.Context
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.users.ffq_app.data.model.FFQItem
import com.users.ffq_app.data.model.PatientRecord
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

object FFQRepository {
    private var cachedItems: List<FFQItem>? = null

    fun loadFFQItems(context: Context): List<FFQItem> {
        cachedItems?.let { return it }
        return try {
            val jsonString = context.assets.open("ffq_database.json").bufferedReader().use { it.readText() }
            val type = object : TypeToken<List<Map<String, Any>>>() {}.type
            val rawList: List<Map<String, Any>> = Gson().fromJson(jsonString, type)
            val list = rawList.map { m ->
                val id = (m["id"] as? Number)?.toInt() ?: (m["id"] as? String)?.toIntOrNull() ?: 0
                val name = m["name"] as? String ?: ""
                val portion = m["portion"] as? String ?: ""
                val notes = m["notes"] as? String ?: ""
                val nutrientKey = m["nutrient_key"] as? String ?: ""
                @Suppress("UNCHECKED_CAST")
                val rawNutrients = m["nutrients"] as? Map<String, Any> ?: emptyMap()
                val nutrients = rawNutrients.mapValues { (_, v) -> (v as? Number)?.toDouble() ?: 0.0 }
                FFQItem(id, name, portion, notes, nutrientKey, nutrients)
            }.sortedBy { it.id }
            cachedItems = list
            list
        } catch (e: Exception) {
            e.printStackTrace()
            emptyList()
        }
    }

    private fun getStorageDir(context: Context): File {
        val dir = File(context.getExternalFilesDir(null), "FFQRecords")
        if (!dir.exists()) dir.mkdirs()
        return dir
    }

    fun saveRecord(context: Context, record: PatientRecord): Boolean {
        return try {
            val dir = getStorageDir(context)
            val file = File(dir, "${record.patientId}_record.json")
            file.writeText(Gson().toJson(record))
            true
        } catch (e: Exception) {
            e.printStackTrace()
            false
        }
    }

    fun getRecord(context: Context, patientId: String): PatientRecord? {
        return try {
            val dir = getStorageDir(context)
            val file = File(dir, "${patientId}_record.json")
            if (file.exists()) {
                Gson().fromJson(file.readText(), PatientRecord::class.java)
            } else null
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }

    fun getAllRecords(context: Context): List<PatientRecord> {
        val dir = getStorageDir(context)
        val files = dir.listFiles { f -> f.extension == "json" } ?: return emptyList()
        return files.mapNotNull { f ->
            try {
                Gson().fromJson(f.readText(), PatientRecord::class.java)
            } catch (e: Exception) {
                null
            }
        }.sortedByDescending { it.timestamp }
    }

    fun deleteRecords(context: Context, patientIds: Set<String>): Boolean {
        val dir = getStorageDir(context)
        patientIds.forEach { id ->
            val file = File(dir, "${id}_record.json")
            if (file.exists()) file.delete()
        }
        return true
    }

    fun formatTimestamp(ts: Long): String {
        return SimpleDateFormat("yyyy/MM/dd HH:mm", Locale.getDefault()).format(Date(ts))
    }
}

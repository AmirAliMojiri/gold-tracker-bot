package com.users.ffq_app.data.model

data class FFQItem(
    val id: Int,
    val name: String,
    val portion: String,
    val notes: String = "",
    val nutrientKey: String = "",
    val nutrients: Map<String, Double> = emptyMap()
)

data class FFQAnswer(
    val day: String = "",
    val week: String = "",
    val month: String = "",
    val year: String = "",
    val userNotes: String = ""
) {
    fun isEmpty(): Boolean = day.isBlank() && week.isBlank() && month.isBlank() && year.isBlank() && userNotes.isBlank()
    
    // Daily equivalent intake frequency
    fun toDailyMultiplier(): Double {
        val d = day.toDoubleOrNull()
        if (d != null && d > 0) return d
        val w = week.toDoubleOrNull()
        if (w != null && w > 0) return w / 7.0
        val m = month.toDoubleOrNull()
        if (m != null && m > 0) return m / 30.42
        val y = year.toDoubleOrNull()
        if (y != null && y > 0) return y / 365.0
        return 0.0
    }
}

data class RegistrationData(
    val id: String = "",
    val diagnosisMO: String = "",
    val marital: Int? = null, // Single=0, Married=1, Divorced=2, Widowed=3
    val otherNarcotics: String = "",
    val ghelian: String = "",
    val cigar: String = "",
    val aspirin: Int? = null, // No=0, Yes=1
    val levotyroxin: Int? = null, // No=0, Yes=1
    val statin: String = "",
    val vitD: Int? = null, // No=0, Yes=1
    val multivitamin: Int? = null, // No=0, Yes=1
    val diabetes: Int? = null, // No=0, Type1=1, Type2=2
    val cvd: Int? = null, // No=0, Yes=1
    val bp: Int? = null, // No=0, Yes=1
    val migrane: Int? = null, // No=0, Yes=1
    val gid: Int? = null, // No=0, Yes=1
    val cancer: Int? = null, // No=0, Yes=1
    val weightKg: String = "",
    val heightCm: String = "",
    val gender: Int? = null, // zan=0, mard=1
    val age: String = "",
    val education: Int? = null, // 0 to 4
    val job: Int? = null, // 0: Khanedar, 1: Bazneshaste, 2: shaghel
    val familySize: String = "",
    val kids: String = "",
    val houseOwnership: Int? = null, // 1: ejarei-rahn, 2: saheb
    // IPAQ fields 2 to 25
    val ipaq: Map<Int, String> = emptyMap(),
    val timestamp: Long = System.currentTimeMillis()
) {
    val bmi: Double? get() {
        val w = weightKg.toDoubleOrNull() ?: return null
        val h = heightCm.toDoubleOrNull() ?: return null
        if (h <= 0) return null
        val hm = h / 100.0
        return w / (hm * hm)
    }

    val ipaqMet: Double get() {
        fun pair(p1: Int, p2: Int, factor: Double): Double {
            val v1 = ipaq[p1]?.toDoubleOrNull() ?: 0.0
            val v2 = ipaq[p2]?.toDoubleOrNull() ?: 0.0
            return v1 * v2 * factor
        }
        return pair(2, 3, 8.0) +
                pair(4, 5, 4.0) +
                pair(6, 7, 3.3) +
                pair(8, 9, 0.0) +
                pair(10, 11, 4.0) +
                pair(12, 13, 3.3) +
                pair(14, 15, 8.0) +
                pair(16, 17, 4.0) +
                pair(18, 19, 3.3) +
                pair(20, 21, 3.3) +
                pair(22, 23, 8.0) +
                pair(24, 25, 4.0)
    }
}

data class PatientRecord(
    val patientId: String,
    val registration: RegistrationData,
    val answers: Map<Int, FFQAnswer> = emptyMap(), // itemId -> FFQAnswer
    val timestamp: Long = System.currentTimeMillis()
)

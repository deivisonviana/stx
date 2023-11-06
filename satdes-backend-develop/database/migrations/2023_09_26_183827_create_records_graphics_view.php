<?php

use Illuminate\Database\Migrations\Migration;


return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        DB::statement("CREATE VIEW records_graphics AS
            SELECT r.id_station, s.name, s.latitude, s.longitude,
                TO_CHAR(r.date_hour, 'YYYY-MM-DD') AS date,
                TO_CHAR(r.date_hour, 'HH24:MI:SS') AS hour,
                MAX(CASE WHEN v.id = 2  THEN r.instant END) AS tem_ins,
                MAX(CASE WHEN v.id = 2  THEN r.maximun END) AS tem_max,
                MAX(CASE WHEN v.id = 2  THEN r.minimun END) AS tem_min,
                MAX(CASE WHEN v.id = 5  THEN r.instant END) AS umd_ins,
                MAX(CASE WHEN v.id = 5  THEN r.maximun END) AS umd_max,
                MAX(CASE WHEN v.id = 5  THEN r.minimun END) AS umd_min,
                MAX(CASE WHEN v.id = 13 THEN r.instant END) AS ven_dir,
                MAX(CASE WHEN v.id = 14 THEN r.instant END) AS ven_vel,
                MAX(CASE WHEN v.id = 15 THEN r.instant END) AS pre_ins
            FROM records AS r
                JOIN stations AS s ON r.id_station = s.id
                JOIN variables AS v ON r.id_variable = v.id
            WHERE r.id_variable IN (2, 5, 13, 14, 15)
            GROUP BY r.id_station, r.date_hour, s.name, s.latitude, s.longitude,
                date, hour;"
        );
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        DB::statement('DROP VIEW IF EXISTS records_graphics');
    }
};

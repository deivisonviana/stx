<?php

namespace Database\Seeders;

use App\Models\Record;
use Illuminate\Database\Seeder;

class RecordSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // Parametros da fabrica
        $totalRecords = 1000000;
        $batchRecords = 10000;

        // Fabrica por lote
        for ($i = 0; $i < $totalRecords; $i += $batchRecords) {
            // Dividindo pelos 5 tipos de variaveis
            $qtdPerType = $batchRecords / 5;

            Record::factory()->temperature()
                ->count($qtdPerType)
                ->create();

            Record::factory()->preasure()
                ->count($qtdPerType)
                ->create();

            Record::factory()->wind_direction()
                ->count($qtdPerType)
                ->create();

            Record::factory()->wind_speed()
                ->count($qtdPerType)
                ->create();

            Record::factory()->precipitation()
                ->count($qtdPerType)
                ->create();
        }
    }
}

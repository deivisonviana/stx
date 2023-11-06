<?php

namespace Database\Seeders;

// use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        $this->call([
            UserSeeder::class,
            StateSeeder::class,
            CountySeeder::class,
            InstituteSeeder::class,
            TypeStationSeeder::class,
            FlagSeeder::class,
            TypeUnitSeeder::class,
            VariableSeeder::class,
            ConfigStationSeeder::class,
            StationSeeder::class,
            //RecordSeeder::class,
        ]);
    }
}

<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class InstituteSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $institutes = [
            [
                'entity' => 'Instituto Capixava de Pesquisa, Assistência Técnica e Extensão Rural',
                'id_user' => 1,
                'id_state' => 8
            ],
            [
                'entity' => 'Cordenadoria Estadual de Protação e Defesa Civil',
                'id_user' => 2,
                'id_state' => 8,
            ],
            [
                'entity' => 'Instituto Nacional de Meteorologia',
                'id_user' => 3,
                'id_state' => 8,
            ],
            [
                'entity' => 'Agência Nacional de Águas e Saneamento Básico',
                'id_user' => 4,
                'id_state' => 8,
            ]
        ];

        DB::table('institutes')->insert($institutes);
    }
}

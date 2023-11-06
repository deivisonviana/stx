<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('config_stations', function (Blueprint $table) {
            // Columns
            $table->id();
            $table->string('model_code');
            $table->json('config');

            // Comment
            $table->comment('Tabela com a configuração dos variaveis mapeadas de um tipo de estação');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('config_stations');
    }
};

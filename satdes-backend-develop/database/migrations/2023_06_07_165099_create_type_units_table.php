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
        Schema::create('type_units', function (Blueprint $table) {
            // Columns
            $table->id();
            $table->string('acronym', 5);
            $table->string('measure', 30);

            // Comment
            $table->comment('Tabela com os tipos unitarios das variaveis');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('type_units');
    }
};

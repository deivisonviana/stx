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
        Schema::create('type_sensors', function (Blueprint $table) {
            // Columns
            $table->id();
            $table->string('model_name', 100);
            $table->string('model_number', 15);
            $table->unsignedBigInteger('id_manufacter');

            // Foreing
            $table->foreign('id_manufacter')->references('id')->on('manufacters');

            // Comment
            $table->comment('Tabela com os tipos de sensores méteorologicos utilizados');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('type_sensors');
    }
};

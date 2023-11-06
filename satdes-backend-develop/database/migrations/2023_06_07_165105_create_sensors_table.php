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
        Schema::create('sensors', function (Blueprint $table) {
            // Columns
            $table->id();
            $table->string('serial_number');
            $table->date('install_date');
            $table->date('removed_date');
            $table->string('asset_number')->nullable();
            $table->unsignedBigInteger('id_station');
            $table->unsignedBigInteger('id_type_sensor');

            // Foreing
            $table->foreign('id_station')->references('id')->on('stations')->onDelete('cascade');
            $table->foreign('id_type_sensor')->references('id')->on('type_sensors');

            // Comment
            $table->comment('Tabela com os sensores cadastrados nas estações');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('sensors');
    }
};

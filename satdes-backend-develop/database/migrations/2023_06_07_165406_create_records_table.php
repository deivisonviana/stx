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
        Schema::create('records', function (Blueprint $table) {
            // Columns
            $table->timestampTz('date_hour');
            $table->decimal('instant');
            $table->decimal('maximun')->nullable();
            $table->decimal('minimun')->nullable();
            $table->decimal('average')->nullable();
            $table->unsignedBigInteger('id_station');
            $table->unsignedBigInteger('id_variable');
            $table->unsignedBigInteger('id_flag');

            // Primary
            $table->primary(['id_station', 'id_variable', 'date_hour']);

            // Foreing
            $table->foreign('id_station')->references('id')->on('stations')->onDelete('cascade');
            $table->foreign('id_variable')->references('id')->on('variables');
            $table->foreign('id_flag')->references('id')->on('flags');

            // Comment
            $table->comment('Tabela com registros méteorologicos individualizados por variavel');
        });

        // Indicates that is a hyper-table
        DB::statement("SELECT create_hypertable('records', 'date_hour')");
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('records');
    }
};

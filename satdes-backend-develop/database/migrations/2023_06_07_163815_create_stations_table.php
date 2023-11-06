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
        Schema::create('stations', function (Blueprint $table) {
            // Columns
            $table->id();
            $table->string('name');
            $table->string('code', 10)->unique();
            $table->text('description')->nullable();
            $table->float('latitude', 8, 6);
            $table->float('longitude', 8, 6);
            $table->decimal('altitude', 6)->nullable();
            $table->boolean('automatic')->default(true);
            $table->date('operation_begin')->nullable();
            $table->date('operation_ended')->nullable();
            $table->unsignedBigInteger('id_config_station')->nullable();
            $table->unsignedBigInteger('id_institute');
            $table->unsignedBigInteger('id_type_station');
            $table->unsignedBigInteger('id_county');
            $table->timestamps();
            $table->softDeletes();

            // Foreing
            $table->foreign('id_config_station')->references('id')->on('config_stations');
            $table->foreign('id_institute')->references('id')->on('institutes')->onDelete('cascade');
            $table->foreign('id_type_station')->references('id')->on('type_stations');
            $table->foreign('id_county')->references('id')->on('counties');

            // Comment
            $table->comment('Tabela com o registro das estações méteorologicas do sistema');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('stations');
    }
};

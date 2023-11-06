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
        Schema::create('readed_files', function (Blueprint $table) {
            // Columns
            $table->id();
            $table->string('file');
            $table->date('date_read')->default(now());
            $table->date('date_make');
            $table->unsignedBigInteger('id_station');
            
            // Foreing
            $table->foreign('id_station')->references('id')->on('stations');

            // Comment
            $table->comment('Tabela para registrar arquivos do FTP lidos.');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('readed_files');
    }
};

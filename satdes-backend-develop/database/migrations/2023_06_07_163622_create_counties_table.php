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
        Schema::create('counties', function (Blueprint $table) {
            // Columns
            $table->id();
            $table->string('name', 75);
            $table->unsignedBigInteger('id_state');

            // Foreing
            $table->foreign('id_state')->references('id')->on('states');

            // Comment
            $table->comment('Tabela com os municipios pertencentes aos estados');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('counties');
    }
};

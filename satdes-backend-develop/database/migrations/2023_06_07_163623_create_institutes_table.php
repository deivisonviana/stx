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
        Schema::create('institutes', function (Blueprint $table) {
            // Columns
            $table->id();
            $table->text('entity');
            $table->unsignedBigInteger('id_state');
            $table->unsignedBigInteger('id_user');

            // Foreign
            $table->foreign('id_state')->references('id')->on('states');
            $table->foreign('id_user')->references('id')->on('users');

            // Comment
            $table->comment('Tabela para registro dos institutos dos quais as etações pertencem');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('institutes');
    }
};

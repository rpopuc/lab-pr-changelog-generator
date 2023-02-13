<?php

namespace App\Domain\Factories;

use App\Domain\Entities\User as UserEntity;

class User
{
    static public function fromArray(array $userData): UserEntity
    {
        return new UserEntity(
            $userData['documentId'] ?? '',
            $userData['name'] ?? '',
            $userData['age'] ?? 0
        );
    }

    static public function fromDocumentId(string $documentId): UserEntity
    {
        return new UserEntity($documentId, '', 0);
    }
}
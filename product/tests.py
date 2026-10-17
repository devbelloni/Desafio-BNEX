from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Produto


class ProdutoModelTests(TestCase):
    def test_str_and_ordering(self):
        Produto.objects.create(nome="Zebra", descricao="d", valor=Decimal("1.00"))
        Produto.objects.create(nome="Abelha", descricao="d", valor=Decimal("2.00"))
        self.assertEqual([str(p) for p in Produto.objects.all()], ["Abelha", "Zebra"])

    def test_negative_price_is_rejected(self):
        with self.assertRaises(ValidationError):
            Produto(nome="x", descricao="d", valor=Decimal("-0.01")).full_clean()

    def test_price_keeps_cents_exactly(self):
        produto = Produto.objects.create(nome="x", descricao="d", valor=Decimal("0.10"))
        produto.refresh_from_db()
        self.assertEqual(produto.valor + Decimal("0.20"), Decimal("0.30"))


class ProdutoViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("ana", password="s3cret-pass")
        cls.produto = Produto.objects.create(nome="Caneta", descricao="Azul", valor=Decimal("3.50"))

    def test_every_view_requires_login(self):
        urls = [
            reverse("produto-list"),
            reverse("produto-add"),
            reverse("produto-detail", args=[self.produto.pk]),
            reverse("produto-update", args=[self.produto.pk]),
            reverse("produto-delete", args=[self.produto.pk]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, url)
            self.assertIn("/admin/login/", response["Location"])

    def test_anonymous_cannot_delete_via_post(self):
        self.client.post(reverse("produto-delete", args=[self.produto.pk]))
        self.assertTrue(Produto.objects.filter(pk=self.produto.pk).exists())

    def test_list_search_and_empty_state(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("produto-list"), {"q": "cane"})
        self.assertContains(response, "Caneta")
        response = self.client.get(reverse("produto-list"), {"q": "xyz"})
        self.assertContains(response, "Nenhum produto encontrado")

    def test_list_is_paginated(self):
        Produto.objects.bulk_create(
            [Produto(nome=f"Item {i:02d}", descricao="d", valor=Decimal("1")) for i in range(15)]
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse("produto-list"))
        self.assertEqual(len(response.context["object_list"]), 10)
        self.assertTrue(response.context["is_paginated"])

    def test_create_update_delete_flow(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("produto-add"), {"nome": "Lápis", "descricao": "HB", "valor": "1.25"}
        )
        self.assertRedirects(response, reverse("produto-list"))
        lapis = Produto.objects.get(nome="Lápis")
        self.assertEqual(lapis.valor, Decimal("1.25"))

        self.client.post(reverse("produto-update", args=[lapis.pk]), {"nome": "Lápis 2B", "descricao": "2B", "valor": "2"})
        lapis.refresh_from_db()
        self.assertEqual((lapis.nome, lapis.valor), ("Lápis 2B", Decimal("2.00")))

        self.client.post(reverse("produto-delete", args=[lapis.pk]))
        self.assertFalse(Produto.objects.filter(pk=lapis.pk).exists())

    def test_invalid_form_is_not_saved(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("produto-add"), {"nome": "Ruim", "descricao": "d", "valor": "-5"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Produto.objects.filter(nome="Ruim").exists())

    def test_detail_404(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("produto-detail", args=[9999])).status_code, 404)

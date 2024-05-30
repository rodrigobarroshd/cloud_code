const functions = require('firebase-functions');
const admin = require('firebase-admin');
const express = require('express');
const cors = require('cors');

admin.initializeApp();
const db = admin.firestore();

const app = express();
app.use(cors({ origin: true }));

// Coleções
const collections = [
  'customers',
  'employees',
  'equipment',
  'keg',
  'merchantUnits',
  'merchants',
  'orders',
  'products',
  'users'
];

// Função para criar endpoints dinamicamente
collections.forEach(collection => {
  // Create a new document
  app.post(`/${collection}/create`, async (req, res) => {
    try {
      const data = req.body;
      const docRef = await db.collection(collection).add(data);
      res.status(201).send({ id: docRef.id });
    } catch (error) {
      res.status(500).send(error.toString());
    }
  });

  // Read a document
  app.get(`/${collection}/read/:id`, async (req, res) => {
    try {
      const docRef = db.collection(collection).doc(req.params.id);
      const doc = await docRef.get();
      if (!doc.exists) {
        res.status(404).send('Document not found');
      } else {
        res.status(200).send(doc.data());
      }
    } catch (error) {
      res.status(500).send(error.toString());
    }
  });

  // Update a document
  app.put(`/${collection}/update/:id`, async (req, res) => {
    try {
      const data = req.body;
      const docRef = db.collection(collection).doc(req.params.id);
      await docRef.update(data);
      res.status(200).send('Document updated');
    } catch (error) {
      res.status(500).send(error.toString());
    }
  });

  // Delete a document
  app.delete(`/${collection}/delete/:id`, async (req, res) => {
    try {
      const docRef = db.collection(collection).doc(req.params.id);
      await docRef.delete();
      res.status(200).send('Document deleted');
    } catch (error) {
      res.status(500).send(error.toString());
    }
  });

  // List all documents
  app.get(`/${collection}`, async (req, res) => {
    try {
      const snapshot = await db.collection(collection).get();
      const docs = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      res.status(200).send(docs);
    } catch (error) {
      res.status(500).send(error.toString());
    }
  });

  // Query documents with filters
  app.get(`/${collection}/query`, async (req, res) => {
    try {
      const { field, operator, value } = req.query;
      const snapshot = await db.collection(collection).where(field, operator, value).get();
      const docs = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      res.status(200).send(docs);
    } catch (error) {
      res.status(500).send(error.toString());
    }
  });
});

exports.api = functions.https.onRequest(app);

const axios = require("axios");
const fs = require("fs");
const path = require("path");
const FormData = require("form-data");
const { v4: uuidv4 } = require("uuid");
const urlModule = require("url");
const YTDlpWrap = require("yt-dlp-wrap").default;
//require('dotenv').config();

// Fonction pour détecter les URLs YouTube
function isYouTubeUrl(url) {
  return (
    url.includes("youtu.be") ||
    url.includes("youtube.com") ||
    url.includes("m.youtube.com")
  );
}

function getExtensionFromUrl(fileUrl) {
  const pathname = urlModule.parse(fileUrl).pathname;
  return path.extname(pathname);
}

// Fonction dédiée au téléchargement YouTube avec installation automatique
async function downloadYouTubeVideo(url, safeName) {
  try {
    console.log(`    Initialisation de yt-dlp...`);
    const ytDlpWrap = new YTDlpWrap();

    // Vérifier/disposer yt-dlp
    try {
      await ytDlpWrap.getVersion();
    } catch {
      console.log(`    Téléchargement de yt-dlp...`);
      await YTDlpWrap.downloadFromGithub();
      console.log(`    yt-dlp installé`);
    }

    // Résoudre ffmpeg (local -> système)
    let ffmpegPath = null;
    try {
      ffmpegPath = require("ffmpeg-static"); // peut être null sur certaines plateformes
    } catch {
      console.warn(
        " ffmpeg-static non trouvé, utilisation du ffmpeg système (PATH)."
      );
    }

    const tempFileName = safeName; //uuidv4();
    const tempDir = path.join(__dirname, "./temp");
    if (!fs.existsSync(tempDir)) fs.mkdirSync(tempDir, { recursive: true });

    const outputTemplate = path.join(tempDir, `${tempFileName}.%(ext)s`);

    console.log(`    Téléchargement YouTube en cours...`);

    const args = [
      url,
      "-o",
      outputTemplate,

      // Sélecteur de formats : H.264 + m4a (compatibles MP4)
      "-f",
      "bv*[ext=mp4][vcodec~='^(avc1|h264)']+ba[ext=m4a]/b[ext=mp4]",

      // Remux/merge en MP4 (nécessite ffmpeg)
      "--merge-output-format",
      "mp4",

      "--no-playlist",
      "--no-warnings",

      // Robustesse
      "--retries",
      "5",
      "--fragment-retries",
      "5",
      "--concurrent-fragments",
      "16",
    ];

    if (ffmpegPath) {
      args.push("--ffmpeg-location", ffmpegPath);
    }

    await ytDlpWrap.execPromise(args);

    // Trouver le fichier sorti (.mp4)
    const files = fs.readdirSync(tempDir);
    const downloadedFile = files.find((f) => f.startsWith(tempFileName));
    if (!downloadedFile) {
      throw new Error("Fichier YouTube non trouvé après téléchargement");
    }

    const finalPath = path.join(tempDir, downloadedFile);

    // Sanity check : extension .mp4
    if (!/\.mp4$/i.test(finalPath)) {
      const extension = getExtensionFromUrl(url);
      const newPath = finalPath.replace(
        path.extname(finalPath),
        `${extension}`
      );
      fs.renameSync(finalPath, newPath);
      console.log(`Renommé en ${path.basename(newPath)}`);
      return newPath;
    }

    console.log(` YouTube téléchargé: ${downloadedFile}`);
    return finalPath;
  } catch (error) {
    throw new Error(`Erreur téléchargement YouTube: ${error.message}`);
  }
}

async function downloadRegularFile(url, safeName) {
  const extension = getExtensionFromUrl(url);
  const tempFilePath = path.join(__dirname, `./temp/${safeName}${extension}`);

  const tempDir = path.dirname(tempFilePath);
  if (!fs.existsSync(tempDir)) {
    fs.mkdirSync(tempDir, { recursive: true });
  }

  const writer = fs.createWriteStream(tempFilePath);

  try {
    const response = await axios({
      url,
      method: "GET",
      responseType: "stream",
      timeout: 30000,
      httpsAgent: new (require("https").Agent)({
        rejectUnauthorized: false,
      }),
    });

    response.data.pipe(writer);

    return new Promise((resolve, reject) => {
      writer.on("finish", () => resolve(tempFilePath));
      writer.on("error", reject);
    });
  } catch (error) {
    // Supprimer le fichier vide en cas d'erreur
    if (fs.existsSync(tempFilePath)) {
      fs.unlinkSync(tempFilePath);
    }

    // Gérer spécifiquement les erreurs 404
    if (error.response && error.response.status === 404) {
      throw new Error(`FICHIER_INTROUVABLE: ${error.response.statusText}`);
    }

    throw error;
  }
}

async function downloadFile(url, safeName) {
  try {
    console.log(`    Téléchargement: ${url.substring(0, 60)}...`);

    if (isYouTubeUrl(url)) {
      return await downloadYouTubeVideo(url, safeName);
    } else {
      return await downloadRegularFile(url, safeName);
    }
  } catch (error) {
    console.error(`    Erreur téléchargement: ${error.message}`);
    throw error;
  }
}
const safeName = "joolise"
downloadFile(
  "https://cdn.videy.co/xOJg70Kv1.mp4",
  (safeName)
);
//module.exports = { downloadFile };
